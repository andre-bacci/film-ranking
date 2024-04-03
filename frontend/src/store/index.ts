import { combineReducers, configureStore } from '@reduxjs/toolkit'
import authReducer from './features/auth/authSlice'
import storage from 'redux-persist/lib/storage' // defaults to localStorage for web
import persistReducer from 'redux-persist/es/persistReducer'
import persistStore from 'redux-persist/es/persistStore'

const appReducer = combineReducers({
  auth: authReducer
})

const persistConfig = {
  key: 'filmranking',
  storage,
  whitelist: [
    "auth"
  ]
}

const persistedReducer = persistReducer(persistConfig, appReducer);

export const store = configureStore({
  reducer: persistedReducer
})

export const persistor = persistStore(store)


export type RootState = ReturnType<typeof store.getState>;
