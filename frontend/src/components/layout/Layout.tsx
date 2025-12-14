import { ReactNode } from 'react';
import Navbar from './Navbar';
import Footer from './Footer';
import WireframeBackground from './WireframeBackground';

interface LayoutProps {
  children: ReactNode;
  showFooter?: boolean;
}

const Layout = ({ children, showFooter = true }: LayoutProps) => {
  return (
    <div className="relative min-h-screen">
      <WireframeBackground />
      <Navbar />
      <main className="relative z-10 pt-24">
        {children}
      </main>
      {showFooter && <Footer />}
    </div>
  );
};

export default Layout;
