import React, { useEffect, useState } from "react";

const CodePen = ({ user, slug, height }) => {
	useEffect(() => {
		const script = document.createElement("script");
		script.src = "https://cpwebassets.codepen.io/assets/embed/ei.js";
		console.log(script);
		script.async = true;
		document.body.appendChild(script);
		return () => {
			document.body.removeChild(script);
		};
	}, []);
	return (
		<div
			className="codepen"
			data-height={height}
			data-theme-id="dark"
			data-default-tab="result"
			data-slug-hash={slug}
			data-editable="true"
			data-user={user}
			style={{ height }}
		></div>
	);
};

export default CodePen;
