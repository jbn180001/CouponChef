"use client";

import { ReactNode, useState } from "react";
import ReactMarkdown from "react-markdown";
import Modal from "../shared/modal";

export default function Card({
  title,
  image,
  description,
  demo,
  large,
  missedIngredients,
  recipe,
  nutrition,
}: {
  title: string;
  image: string;
  description: string;
  demo: ReactNode;
  large?: boolean;
  missedIngredients: string;
  recipe: string;
  nutrition: string;
}) {

  const [isModalVisible1, setIsModalVisible1] = useState(false);
  const [isModalVisible2, setIsModalVisible2] = useState(false);
  const [isModalVisible3, setIsModalVisible3] = useState(false);

  return (
    <>
      <Modal showModal={isModalVisible1} setShowModal={setIsModalVisible1}>
        <div style={{ textAlign: 'center', paddingTop: '20px' }}> {/* Centers content horizontally */}
          <span style={{ fontSize: '48px' }}>🔎</span>
        </div>
        <div style={{ padding: '20px', position: 'relative' }}> {/* Adjust the padding as needed */}
          {missedIngredients}
        </div>
      </Modal>
      <Modal showModal={isModalVisible2} setShowModal={setIsModalVisible2}>
        <div style={{ textAlign: 'center', paddingTop: '20px' }}> {/* Centers content horizontally */}
          <span style={{ fontSize: '48px' }}>🥗</span>
        </div>
        <div style={{ padding: '20px', position: 'relative' }}> {/* Adjust the padding as needed */}
          {nutrition}
        </div>
      </Modal>
      <Modal showModal={isModalVisible3} setShowModal={setIsModalVisible3}>
        <div style={{ textAlign: 'center', paddingTop: '20px' }}> {/* Centers content horizontally */}
          <span style={{ fontSize: '48px' }}>🍳</span>
        </div>
        <div style={{ padding: '20px', position: 'relative' }}> {/* Adjust the padding as needed */}
          {recipe}
        </div>
      </Modal>
      <div
        className={`relative col-span-1 h-196 overflow-hidden rounded-xl border border-gray-200 bg-white shadow-md ${large ? "md:col-span-2" : ""
          }`}
        style={{ height: '500px' }}
      >
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '20px', paddingBottom: '20px' }}>
          <img src={image} style={{ borderRadius: '10px' }} />
        </div>

        <div className="mx-auto max-w-md text-center">
          <h2 className="bg-gradient-to-br from-black to-stone-500 bg-clip-text font-display text-xl font-bold text-transparent [text-wrap:balance] md:text-3l md:font-normal">
            {title}
          </h2>
          <div className="prose-sm mt-3 leading-normal text-gray-500 [text-wrap:balance] md:prose">
            <ReactMarkdown
              components={{
                a: ({ node, ...props }) => (
                  <a
                    target="_blank"
                    rel="noopener noreferrer"
                    {...props}
                    className="font-medium text-gray-800 underline transition-colors"
                  />
                ),
                code: ({ node, ...props }) => (
                  <code
                    {...props}
                    // @ts-ignore (to fix "Received `true` for a non-boolean attribute `inline`." warning)
                    inline="true"
                    className="rounded-sm bg-gray-100 px-1 py-0.5 font-mono font-medium text-gray-800"
                  />
                ),
              }}
            >
              {description}
            </ReactMarkdown>
          </div>
          <br>
          </br>
          <div>
            <button onClick={() => setIsModalVisible1(true)}>Missing Ingredients 🔎</button>

          </div>
          <div>
            <button onClick={() => setIsModalVisible2(true)}>Nutrition Facts 🥗</button>

          </div>
          <div>
            <button onClick={() => setIsModalVisible3(true)}>Read Full Recipe 🍽️</button>

          </div>
        </div>
      </div >
    </>
  );
}
