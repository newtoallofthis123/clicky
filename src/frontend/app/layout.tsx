import './globals.css'

export const metadata = {
    title: 'Cache | Your Hospitals Digital Front Door',
    description: 'Your Hospitals Digital Front Door',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
      <html lang="en">
          <head>
              <link rel="icon" href="icon.svg" />
              <link rel="preconnect" href="https://fonts.googleapis.com" />
              <link
                  rel="preconnect"
                  href="https://fonts.gstatic.com"
                  crossOrigin="anonymous"
        />
          {/* //@ts-ignore */}
          <link
              href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Inter:wght@400;700&family=Archivo+Black&family=Scheherazade+New:wght@400;700&display=swap"
              rel="stylesheet"
          />
          </head>
          <body>{children}</body>
      </html>
  );
}
