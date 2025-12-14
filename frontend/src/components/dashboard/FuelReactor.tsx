import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Zap, Sparkles } from 'lucide-react';
import QRCode from 'react-qr-code';
import { api } from '@/lib/api';
import { toast } from 'sonner';

interface FuelReactorProps {
  isOpen: boolean;
  onClose: () => void;
}

const FuelReactor = ({ isOpen, onClose }: FuelReactorProps) => {
  const [amount, setAmount] = useState(100);
  const [message, setMessage] = useState('');
  const [paymentUrl, setPaymentUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleInitiateTransfer = async () => {
    setIsLoading(true);
    try {
      const response = await api.post('/api/payment/generate-link', {
        amount,
        message,
      });
      setPaymentUrl(response.data.payment_url);
      toast.success('Payment link generated! Scan the QR code.');
    } catch (error) {
      toast.error('Failed to generate payment link');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setPaymentUrl(null);
    setMessage('');
    setAmount(100);
    onClose();
  };

  const powerPercentage = ((amount - 10) / (1000 - 10)) * 100;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
        >
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-background/80 backdrop-blur-md"
            onClick={handleClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="relative w-full max-w-md bg-card/60 backdrop-blur-xl border border-primary/30 rounded-2xl p-6 shadow-2xl shadow-primary/20"
          >
            {/* Close Button */}
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 text-muted-foreground hover:text-foreground transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Header */}
            <div className="text-center mb-6">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
                className="inline-block mb-3"
              >
                <div className="w-16 h-16 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center">
                  <Zap className="w-8 h-8 text-primary" />
                </div>
              </motion.div>
              <h2 className="text-2xl font-bold text-foreground">Fuel the Algorithm</h2>
              <p className="text-muted-foreground text-sm mt-1">Power up the reactor core</p>
            </div>

            {!paymentUrl ? (
              <>
                {/* Power Level Slider */}
                <div className="mb-6">
                  <div className="flex justify-between items-center mb-2">
                    <label className="text-sm font-medium text-foreground">Power Level</label>
                    <span className="text-primary font-mono text-lg">₹{amount}</span>
                  </div>
                  
                  {/* Custom Slider Container */}
                  <div className="relative h-3 bg-muted rounded-full overflow-hidden">
                    <motion.div
                      className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary/50 to-primary rounded-full"
                      style={{ width: `${powerPercentage}%` }}
                      animate={{ width: `${powerPercentage}%` }}
                      transition={{ type: 'spring', damping: 20 }}
                    />
                    <input
                      type="range"
                      min="10"
                      max="1000"
                      step="10"
                      value={amount}
                      onChange={(e) => setAmount(Number(e.target.value))}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <motion.div
                      className="absolute top-1/2 -translate-y-1/2 w-5 h-5 bg-primary rounded-full shadow-lg shadow-primary/50 border-2 border-foreground"
                      style={{ left: `calc(${powerPercentage}% - 10px)` }}
                      animate={{ left: `calc(${powerPercentage}% - 10px)` }}
                      transition={{ type: 'spring', damping: 20 }}
                    />
                  </div>
                  
                  <div className="flex justify-between text-xs text-muted-foreground mt-1">
                    <span>₹10</span>
                    <span>₹1000</span>
                  </div>
                </div>

                {/* Support Message */}
                <div className="mb-6">
                  <label className="text-sm font-medium text-foreground mb-2 block">
                    Transmission Message
                  </label>
                  <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Leave a message for the reactor..."
                    className="w-full h-24 bg-muted/50 border border-primary/20 rounded-xl p-3 text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 resize-none transition-all"
                  />
                </div>

                {/* CTA Button */}
                <motion.button
                  onClick={handleInitiateTransfer}
                  disabled={isLoading}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-4 bg-primary/20 border border-primary text-primary font-bold rounded-xl hover:bg-primary/30 hover:shadow-lg hover:shadow-primary/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isLoading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                    >
                      <Sparkles className="w-5 h-5" />
                    </motion.div>
                  ) : (
                    <>
                      <Zap className="w-5 h-5" />
                      INITIATE TRANSFER
                    </>
                  )}
                </motion.button>
              </>
            ) : (
              /* QR Code Display */
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-center"
              >
                <p className="text-muted-foreground text-sm mb-4">
                  Scan to complete power transfer
                </p>
                <div className="inline-block p-4 bg-white rounded-xl">
                  <QRCode
                    value={paymentUrl}
                    size={200}
                    bgColor="#ffffff"
                    fgColor="#0a0a0a"
                  />
                </div>
                <p className="text-primary font-mono text-lg mt-4">₹{amount}</p>
                <motion.button
                  onClick={() => setPaymentUrl(null)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="mt-4 px-6 py-2 bg-muted border border-primary/30 text-foreground rounded-lg hover:bg-muted/80 transition-all"
                >
                  Generate New Code
                </motion.button>
              </motion.div>
            )}

            {/* Decorative Elements */}
            <div className="absolute -top-1 -left-1 w-3 h-3 border-t-2 border-l-2 border-primary rounded-tl-lg" />
            <div className="absolute -top-1 -right-1 w-3 h-3 border-t-2 border-r-2 border-primary rounded-tr-lg" />
            <div className="absolute -bottom-1 -left-1 w-3 h-3 border-b-2 border-l-2 border-primary rounded-bl-lg" />
            <div className="absolute -bottom-1 -right-1 w-3 h-3 border-b-2 border-r-2 border-primary rounded-br-lg" />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default FuelReactor;
