(ns nand2tetris-assembler.core
  (:gen-class))

(require '[clojure.string :as str])

(defn -main
	"I don't do a whole lot ... yet."
	[& args]
	prinln(remove #(or (re-matches #"//.*" %) (str/blank? %)) (map str/trim ( str/split-lines (slurp (first args)))))


	;println(lines)
	
)
