import { useEffect, useRef, useState } from "react";

/**
 * Hook that detects when an element enters the viewport and triggers a reveal.
 * @param {object} options
 * @param {number} options.threshold - 0 to 1 visibility ratio (default 0.15)
 * @param {number} options.delay - delay in ms before marking as visible (default 0)
 * @returns {{ ref, isVisible }}
 */
export function useScrollReveal({ threshold = 0.15, delay = 0 } = {}) {
  const ref = useRef(null);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          if (delay > 0) {
            setTimeout(() => setIsVisible(true), delay);
          } else {
            setIsVisible(true);
          }
          observer.unobserve(element);
        }
      },
      { threshold }
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [threshold, delay]);

  return { ref, isVisible };
}
