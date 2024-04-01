import { useEffect } from "react";
import { Route, Routes, useLocation } from "react-router-dom";

import {
	Home
} from "pages";


function Routers() {
	const { pathname } = useLocation();

	useEffect(() => {
		setTimeout(() => {
			window.scrollTo({
				top: 0,
				left: 0,
				behavior: "smooth"
			});
		}, 100);
	}, [pathname]);

	return (
		<Routes>
			<Route path="/" element={<Home />} />
		</Routes>
	);
}

export default Routers;
