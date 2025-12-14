import { motion } from 'framer-motion';

const WireframeBackground = () => {
  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-void opacity-80" />
      
      {/* Floating particles */}
      <div className="absolute inset-0">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 rounded-full bg-neon/30"
            initial={{
              x: Math.random() * (typeof window !== 'undefined' ? window.innerWidth : 1000),
              y: Math.random() * (typeof window !== 'undefined' ? window.innerHeight : 800),
            }}
            animate={{
              y: [null, Math.random() * -200, null],
              opacity: [0.2, 0.6, 0.2],
            }}
            transition={{
              duration: 5 + Math.random() * 5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: Math.random() * 5,
            }}
          />
        ))}
      </div>

      {/* 3D Wireframe Cube */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
        <motion.div
          className="relative w-[400px] h-[400px]"
          style={{ perspective: '1000px' }}
        >
          <motion.div
            className="absolute inset-0"
            style={{ transformStyle: 'preserve-3d' }}
            animate={{
              rotateX: [0, 360],
              rotateY: [0, 360],
            }}
            transition={{
              duration: 30,
              repeat: Infinity,
              ease: "linear",
            }}
          >
            {/* Cube faces - wireframe style */}
            {[
              { transform: 'translateZ(100px)', rotate: '' },
              { transform: 'translateZ(-100px)', rotate: 'rotateY(180deg)' },
              { transform: 'translateX(100px)', rotate: 'rotateY(90deg)' },
              { transform: 'translateX(-100px)', rotate: 'rotateY(-90deg)' },
              { transform: 'translateY(-100px)', rotate: 'rotateX(90deg)' },
              { transform: 'translateY(100px)', rotate: 'rotateX(-90deg)' },
            ].map((face, i) => (
              <div
                key={i}
                className="absolute w-[200px] h-[200px] border border-neon/20"
                style={{
                  transform: `${face.transform} ${face.rotate}`,
                  left: '100px',
                  top: '100px',
                }}
              />
            ))}
            
            {/* Corner connectors */}
            {[...Array(12)].map((_, i) => (
              <motion.div
                key={`line-${i}`}
                className="absolute w-[2px] h-[200px] bg-gradient-to-b from-neon/30 via-neon/10 to-transparent"
                style={{
                  transformOrigin: 'center',
                  left: '200px',
                  top: '100px',
                  transform: `rotateZ(${i * 30}deg) translateX(${50 + i * 5}px)`,
                }}
              />
            ))}
          </motion.div>
        </motion.div>
      </div>

      {/* Secondary geometric shape - Icosahedron approximation */}
      <motion.div
        className="absolute top-1/4 right-1/4 w-32 h-32"
        style={{ perspective: '500px' }}
      >
        <motion.div
          className="relative w-full h-full"
          style={{ transformStyle: 'preserve-3d' }}
          animate={{
            rotateX: [0, -360],
            rotateY: [0, 360],
            rotateZ: [0, 180],
          }}
          transition={{
            duration: 45,
            repeat: Infinity,
            ease: "linear",
          }}
        >
          {[0, 72, 144, 216, 288].map((angle, i) => (
            <div
              key={i}
              className="absolute w-full h-full border-l border-neon/15"
              style={{
                transform: `rotateY(${angle}deg) translateZ(40px)`,
              }}
            />
          ))}
        </motion.div>
      </motion.div>

      {/* Glowing orb */}
      <motion.div
        className="absolute bottom-1/4 left-1/4 w-64 h-64 rounded-full"
        style={{
          background: 'radial-gradient(circle, hsl(142 69% 58% / 0.1) 0%, transparent 70%)',
        }}
        animate={{
          scale: [1, 1.2, 1],
          opacity: [0.3, 0.5, 0.3],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Grid lines */}
      <div 
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `
            linear-gradient(hsl(142 69% 58%) 1px, transparent 1px),
            linear-gradient(90deg, hsl(142 69% 58%) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
        }}
      />
    </div>
  );
};

export default WireframeBackground;
