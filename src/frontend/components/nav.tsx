import React from 'react'
import Image from 'next/image';
import Link from 'next/link';

type Props = {}

export default function Nav({}: Props) {
  return (
      <>
          <nav>
              <div
                  style={{
                      boxShadow: '0 0 2px 2px #797979',
                  }}
                  className="flex flex-row border-2 border-black justify-between items-center p-4"
              >
                  <div className="flex-shrink-0 flex flex-row justify-around">
                      <Image
                          width={162}
                          height={162}
                          className="w-10 h-10 md:w-12 md:h-12"
                          src="icon.svg"
                          alt="NoobScience Logo"
                      />
                      <h1 className="text-3xl font-bold p-1 ml-2">
                          <a href="/">Clicky</a>
                      </h1>
                  </div>
                  <div className="gap-x-10">
                      <ul className="gap-x-8 flex flex-row">
                          {[
                              'about',
                              'dashboard',
                              'records',
                              'archive',
                              'add',
                              'manage',
                          ].map((link) => {
                              return (
                                  <li className="text-lg" key={link}>
                                      <Link href={link}>
                                          {link.slice(0, 1).toUpperCase() +
                                              link.slice(1)}
                                      </Link>
                                  </li>
                              );
                          })}
                      </ul>
                  </div>
                  <div className="border-2 p-1 border-gray-600 rounded-3xl">
                      <div>
                          <input
                              type="search"
                              placeholder="Type to Search anything"
                              className="w-80 text-center text-sm px-1 hover:outline-none focus:outline-none"
                              name="search"
                              id="search"
                          />
                          <button type="submit">🔍</button>
                      </div>
                  </div>
                  <div>
                      <button className="text-gray-900 font-bold py-2 px-4 rounded">
                          🏥 Hospital
                      </button>
                  </div>
              </div>
          </nav>
      </>
  );
}