import React from "react";

export default function Marker({ children, color = "greenyellow" }) {
	return (
		<em
			style={{
				background: `linear-gradient(to top, transparent 0, ${color} 0, ${color} 0.3em, transparent 0)`,
				fontSize: "120%",
				fontWeight: "bold",
				fontStyle: "normal",
			}}
		>
			{children}
		</em>
	);
}
