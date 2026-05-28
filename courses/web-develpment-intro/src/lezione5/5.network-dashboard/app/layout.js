import "./globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="it">
      <body className="bg-gray-50">{children}</body>
    </html>
  );
}
