import React from "react";

const App = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-green-500">SYSTEM CHECK: ONLINE ✅</h1>
        <p className="text-xl">
          If you can see this, your Vercel deployment is PERFECT.
        </p>
        <p className="text-gray-400">
          The blank screen was caused by the AuthProvider or Router.
        </p>
      </div>
    </div>
  );
};

export default App;
