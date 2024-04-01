from typing import Iterable, List, Optional, OrderedDict

from django.db.models import Model, Q, QuerySet

from .objects import set_all_attrs


class NestedSerializerManyRelationHandler:
    def __init__(
        self,
        parent_instance: Model,
        related_model: type[Model],
        related_queryset: QuerySet,
        reverse_relationship_name: Optional[str] = "",
    ):
        """
        :param Model parent_instance: the parent object
        :param type(Model) related_model: the child's Model class
        :param QuerySet related_queryset: the `related_queryset` from the parent
            (such as `instance.child_relation.all()`)
        :param Optional[str] reverse_relationship_name: pass it if you need the child
        to receive the parent's ID during creation (for example, if the child references
        the parent as `parent_name` you may pass `"parent_name"` and it will be injected
        in the child instance's data).
        """
        self.related_model: type[Model] = related_model
        self.related_queryset: QuerySet = related_queryset
        self.parent_instance: Model = parent_instance
        self.reverse_relationship_name: Optional[str] = reverse_relationship_name

    # Deletion

    def select_objects_to_delete(self, related_data: Iterable[OrderedDict]) -> QuerySet:
        """
        Implements and applies filters to the `related_queryset`, selecting the objects
        that need deletion. By default, selects those present in the database but whose
        id is absent in the `related_data`.
        """
        current_related_objects = self.related_queryset.all()
        incoming_object_ids = [
            item["id"] for item in related_data if item.get("id") is not None
        ]
        related_objects_to_delete = current_related_objects.filter(
            ~Q(id__in=incoming_object_ids)
        )
        return related_objects_to_delete

    def delete_related_objects(self, related_data: Iterable[OrderedDict]):
        """
        `.delete()`s the elements selected by the `select_objects_to_delete` method. By default,
        it deletes objects present in the database but with no id present in the passed `related_data`.

        It is advisable to perform this operation before creating new objects, as their `id`s
        will not be present in the `related_data` as well.
        """
        return self.select_objects_to_delete(related_data).delete()

    # Update

    def select_objects_to_update(self, related_data: Iterable[OrderedDict]) -> QuerySet:
        """
        Implements and applies filters to the `related_queryset`, selecting the objects
        that need update. By default, selects those with an `"id"` key in the `related_data`
        record.
        """
        incoming_object_ids = [
            item["id"] for item in related_data if item.get("id") is not None
        ]
        current_objects_to_update = self.related_queryset.filter(
            Q(id__in=incoming_object_ids)
        )
        return current_objects_to_update

    def map_update_records(self, related_data: Iterable[OrderedDict]) -> dict:
        """
        Creates a dict mapping a unique key and a dict of update data to be used later
        by the `get_object_update_data` method. By default, uses the stringified `"id"` field.
        """
        return {
            str(item["id"]): {**item}
            for item in related_data
            if item.get("id") is not None
        }

    def get_object_update_data(
        self, db_item: Model, update_data_map: dict
    ) -> OrderedDict:
        """
        Implements a way to find a database object's update data in the mapping created by
        the `map_update_records` method. By default, uses the object's stringified primary key.
        """
        return update_data_map.get(str(db_item.pk))

    def update_related_objects(
        self, related_data: Iterable[OrderedDict], update_fields: Iterable[str]
    ):
        """
        `.bulk_update()`s the elements selected by the `select_objects_to_update` method. By default,
        selects those with an `'id'` field passed in the `related_data` record.

        Make sure to include extra fields such as the parent's `id` in the children (related)
        data records beforehand.
        """
        current_objects_to_update = self.select_objects_to_update(related_data)
        update_data_record = self.map_update_records(related_data)
        update_objects: List[Model] = [
            set_all_attrs(
                db_item, self.get_object_update_data(db_item, update_data_record)
            )
            for db_item in current_objects_to_update
        ]
        self.related_model.objects.bulk_update(update_objects, update_fields)
        return update_objects

    # Creation

    def _inject_parent(self, related_data: Iterable[OrderedDict]):
        return [
            {**item, self.reverse_relationship_name: self.parent_instance}
            for item in related_data
        ]

    def select_records_to_create(
        self, related_data: Iterable[OrderedDict]
    ) -> Iterable[OrderedDict]:
        """
        Selects the records to be created.  By default selects those without an `'id'` field
        passed in the `related_data` record.
        """
        return [item for item in related_data if item.get("id") is None]

    def create_related_objects(self, related_data: Iterable[OrderedDict]):
        """
        `bulk_create`s the records selected by the `select_records_to_create` method. By default,
        selects those without an `'id'` field passed in the `related_data` record.

        If the `reverse_relationship_name` optional argument was provided, also includes
        the parent's `id` in the children (related) data records beforehand.

        Also sets a temp_id in the created objects if this key is present in the data record.
        """
        create_data_list = self.select_records_to_create(related_data)
        if self.reverse_relationship_name:
            create_data_list = self._inject_parent(create_data_list)

        temp_ids = [item.pop("temp_id", None) for item in create_data_list]
        objects_to_create = [
            self.related_model(**record) for record in create_data_list
        ]
        created_objects = self.related_model.objects.bulk_create(objects_to_create)

        for idx, temp_id in enumerate(temp_ids):
            object_instance = created_objects[idx]
            object_instance.temp_id = temp_id
        return created_objects

    # Entrypoint
    def handle_relation(
        self,
        data: Iterable[OrderedDict],
        update_fields: Iterable[str] = None,
        many_fields: Iterable[str] = None,
    ):
        if update_fields is None:
            update_fields = []
        if many_fields is None:
            many_fields = []
        data_copy = [
            {k: v for k, v in data_item.items() if k not in many_fields}
            for data_item in data
            if data_item is not None
        ]
        deleted_objects = self.delete_related_objects(data_copy)
        created_objects = self.create_related_objects(data_copy)
        updated_objects = self.update_related_objects(data_copy, update_fields)
        return (created_objects, updated_objects, deleted_objects)
