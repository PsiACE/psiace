import { getAllSlides } from "@/data/post";
import { siteConfig } from "@/site.config";
import rss from "@astrojs/rss";

export const GET = async () => {
	const slides = await getAllSlides();

	return rss({
		title: siteConfig.title,
		description: siteConfig.description,
		site: import.meta.env.SITE,
		items: slides.map((slide) => ({
			title: slide.data.title,
			description: slide.data.description,
			pubDate: slide.data.publishDate,
			link: `slides/${slide.id}/`,
		})),
	});
};
