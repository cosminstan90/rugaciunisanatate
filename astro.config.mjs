import node from "@astrojs/node";
import react from "@astrojs/react";
import { defineConfig, fontProviders } from "astro/config";
import emdash, { local } from "emdash/astro";
import { postgres } from "emdash/db";

export default defineConfig({
	output: "server",
	adapter: node({ mode: "standalone" }),
	image: {
		layout: "constrained",
		responsiveStyles: true,
	},
	integrations: [
		react(),
		emdash({
			database: postgres({
				connectionString: process.env.DATABASE_URL,
			}),
			storage: local({
				directory: "./uploads",
				baseUrl: "/_emdash/api/media/file",
			}),
		}),
	],
	fonts: [
		{
			provider: fontProviders.google(),
			name: "Cormorant Garamond",
			cssVariable: "--font-display",
			weights: [300, 400, 500, 600, 700],
			styles: ["normal", "italic"],
			fallbacks: ["Georgia", "serif"],
		},
		{
			provider: fontProviders.google(),
			name: "Lora",
			cssVariable: "--font-body",
			weights: [400, 500],
			styles: ["normal", "italic"],
			fallbacks: ["Georgia", "serif"],
		},
	],
	devToolbar: { enabled: false },
	site: "https://rugaciunisanatate.ro",
});
