import React, { useEffect, useState } from "react";
import axios from "axios";

const LinkCard = ({ url }) => {
	console.log(url);
	const [metadata, setMetadata] = useState(null);

	useEffect(() => {
		const fetchMetadata = async () => {
			try {
				const response = await fetch("/_dev" + url);
				console.log(response.text());
				setMetadata(response.data);
			} catch (error) {
				console.error("Error fetching metadata:", error);
			}
		};

		fetchMetadata();
	}, [url]);

	if (!metadata) {
		return null; // メタデータが読み込まれるまで何も表示しない
	}

	return (
		<div className="link-card">
			<div className="thumbnail">
				<img src={metadata.thumbnailUrl} alt="Thumbnail" />
			</div>
			<div className="details">
				<h2>{metadata.title}</h2>
				<p>{metadata.description}</p>
				{/* その他のメタデータを表示する */}
			</div>
		</div>
	);
};

export default LinkCard;
