"use client";

import Card from "@/components/home/card";
import { DEPLOY_URL } from "@/lib/constants";
import { Github, Twitter } from "@/components/shared/icons";
import WebVitals from "@/components/home/web-vitals";
import ComponentGrid from "@/components/home/component-grid";
import Image from "next/image";
import { nFormatter } from "@/lib/utils";

// import data from '../../../recipes_output'
import getFoodItems from '../app/services/FoodService';
import { useEffect, useState } from "react";

interface nutritiontype { Calories: string, Fat: string, Carbohydrates: string, Sodium: string, Protein: string, Fiber: string }
interface DataType { title: string, image: string, usedIngredients: string[], missedIngredients: string[], nutrition: nutritiontype, instructions: string[] }

export default function Home({ }: {}) {
  // export default async function Home() => {
  const [data, setData] = useState<DataType[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const res = await fetch("http://127.0.0.1:8080/getrecipes", {
        method: 'GET',
      });

      if (res.ok) {
        const data = JSON.parse(await res.json());
        console.log(data)
        // const data_array: DataType[] = Object.entries(data)
        // const datavar: DataType = { title: data.title, image: data.image, usedIngredients: data.usedIngredients, missedIngredients: data.missedIngredients, nutrition: data.nutrition, instructions: data.instructions }
        setData(data);
      } else {
        console.error('Failed to fetch:', res.statusText);
      }
    };

    fetchData();
  }, []);


  // export default async function Home() {
  // const { stargazers_count: stars } = await fetch(
  //   "https://api.github.com/repos/steven-tey/precedent",
  //   {
  //     ...(process.env.GITHUB_OAUTH_TOKEN && {
  //       headers: {
  //         Authorization: `Bearer ${process.env.GITHUB_OAUTH_TOKEN}`,
  //         "Content-Type": "application/json",
  //       },
  //     }),
  //     // data will revalidate every 24 hours
  //     next: { revalidate: 86400 },
  //   },
  // )
  //   .then((res) => res.json())
  //   .catch((e) => console.log(e));

  return (
    <>
      <div className="z-10 w-full max-w-xl px-5 xl:px-0">
        <h1
          className="animate-fade-up bg-gradient-to-br from-black to-stone-500 bg-clip-text text-center font-display text-4xl font-bold tracking-[-0.02em] text-transparent opacity-0 drop-shadow-sm [text-wrap:balance] md:text-7xl md:leading-[5rem]"
          style={{ animationDelay: "0.15s", animationFillMode: "forwards" }}
        >
          Here are your weekly recipes
        </h1>
        <p
          className="mt-6 animate-fade-up text-center text-gray-500 opacity-0 [text-wrap:balance] md:text-xl"
          style={{ animationDelay: "0.25s", animationFillMode: "forwards" }}
        >
          Scroll to find meals, nutrition facts, and ingredients.
        </p>
        <div
          className="mx-auto mt-6 flex animate-fade-up items-center justify-center space-x-5 opacity-0"
          style={{ animationDelay: "0.3s", animationFillMode: "forwards" }}
        >
          <a
            className="group flex max-w-fit items-center justify-center space-x-2 rounded-full border border-black bg-black px-5 py-2 text-sm text-white transition-colors hover:bg-white hover:text-black"
            href={DEPLOY_URL}
            target="_blank"
            rel="noopener noreferrer"
          >
            <svg
              className="h-4 w-4 group-hover:text-black"
              viewBox="0 0 24 24"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M12 4L20 20H4L12 4Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            <p>Share</p>
          </a>
          <a
            className="flex max-w-fit items-center justify-center space-x-2 rounded-full border border-gray-300 bg-white px-5 py-2 text-sm text-gray-600 shadow-md transition-colors hover:border-gray-800"
            target="_blank"
            rel="noopener noreferrer"
          >
            {/* <Github /> */}
            <p>
              <span className="hidden sm:inline-block">Download</span>
            </p>
          </a>
        </div>
      </div>
      <div className="my-10 grid w-full max-w-screen-xl animate-fade-up grid-cols-1 gap-5 px-5 md:grid-cols-3 xl:px-0">
        {data ?
          data.map((card) => (
            < Card
              key={card.title}
              title={card.title}
              image={card.image}
              description={card.usedIngredients.join(', ')}
              missedIngredients={card.missedIngredients.join(', ')}
              nutrition={
                // ""
                <>
                  <p>Calories: {card.nutrition.Calories}</p>
                  <p>Protein: {card.nutrition.Protein}</p>
                  <p>Carbs: {card.nutrition.Carbohydrates}</p>
                  <p>Fats: {card.nutrition.Fat}</p>
                  <p>Sodium: {card.nutrition.Sodium}</p>
                  <p>Fiber: {card.nutrition.Fiber}</p>
                </>
              }
              recipe={
                // ""
                card.instructions.map((instruction, index) => (
                  <p key={index}>{instruction}</p>
                ))
              }
              demo={
                card.title === "Beautiful, reusable components" ? (
                  <ComponentGrid />
                ) : (
                    card.title
                  )
              }
              large={false}
            />
          )) : null}
      </div>
    </>
  );
}

const features = [
  {
    title: "Curry Chicken Salad",
    // image: "https://spoonacular.com/recipeImages/651437-312x231.jpg"
    description:
      "Pre-built beautiful, a11y-first components, powered by [Tailwind CSS](https://tailwindcss.com/), [Radix UI](https://www.radix-ui.com/), and [Framer Motion](https://framer.com/motion)",
    large: false,
  },
  {
    title: "Beautiful, reusable components",
    description:
      "Pre-built beautiful, a11y-first components, powered by [Tailwind CSS](https://tailwindcss.com/), [Radix UI](https://www.radix-ui.com/), and [Framer Motion](https://framer.com/motion)",
    large: false,
  },

  {
    title: "Performance first",
    description:
      "Built on [Next.js](https://nextjs.org/) primitives like `@next/font` and `next/image` for stellar performance.",
    demo: <WebVitals />,
  },
  // {
  //   title: "One-click Deploy",
  //   description:
  //     "Jumpstart your next project by deploying Precedent to [Vercel](https://vercel.com/) in one click.",
  //   demo: (
  //     <a href={DEPLOY_URL}>
  //       <Image
  //         src="https://vercel.com/button"
  //         alt="Deploy with Vercel"
  //         width={120}
  //         height={30}
  //         unoptimized
  //       />
  //     </a>
  //   ),
  // },
  // {
  //   title: "Built-in Auth + Database",
  //   description:
  //     "Precedent comes with authentication and database via [Auth.js](https://authjs.dev/) + [Prisma](https://prisma.io/)",
  //   demo: (
  //     <div className="flex items-center justify-center space-x-20">
  //       <Image alt="Auth.js logo" src="/authjs.webp" width={50} height={50} />
  //       <Image alt="Prisma logo" src="/prisma.svg" width={50} height={50} />
  //     </div>
  //   ),
  // },
  // {
  //   title: "Hooks, utilities, and more",
  //   description:
  //     "Precedent offers a collection of hooks, utilities, and `@vercel/og`",
  //   demo: (
  //     <div className="grid grid-flow-col grid-rows-3 gap-10 p-10">
  //       <span className="font-mono font-semibold">useIntersectionObserver</span>
  //       <span className="font-mono font-semibold">useLocalStorage</span>
  //       <span className="font-mono font-semibold">useScroll</span>
  //       <span className="font-mono font-semibold">nFormatter</span>
  //       <span className="font-mono font-semibold">capitalize</span>
  //       <span className="font-mono font-semibold">truncate</span>
  //     </div>
  //   ),
  // },
];
