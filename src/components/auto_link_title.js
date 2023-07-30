import React, { useEffect, useState } from "react";

const AutoLinkTitle = ({ url }) => {
	const [posts, setPosts] = useState([]);

	var rootURL = "https://fereria.github.io/reincarnation_tech";

	useEffect(() => {
		fetchData(url);
	}, []);

	const fetchData = async (url) => {
		fetch(rootURL + url, { method: "GET" })
			.then((res) => res.text())
			.then((data) => {
				setPosts(data.match(/<header><h1>(.*?)\<\/h1><\/header>/i)[1]);
			})
			.catch((error) => {
				// Errorだった場合、URLを文字列にする
				setPosts(rootURL + url);
			});
	};

	return <a href={rootURL + url}>{posts}</a>;
};

export default AutoLinkTitle;
