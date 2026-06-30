#!/usr/bin/env sbcl --script
;;; A minimal self-rewriting Lisp program
;;; This program increments its own counter each time it runs

(defparameter *generation* 0)

(defun read-self ()
  "Read this program's source code"
  (with-open-file (stream "self-rewriting.lisp")
    (let ((contents (make-string (file-length stream))))
      (read-sequence contents stream)
      contents)))

(defun write-self (code)
  "Write modified code back to this file"
  (with-open-file (stream "self-rewriting.lisp"
                          :direction :output
                          :if-exists :supersede)
    (write-sequence code stream)))

(defun increment-generation (code)
  "Increment the generation counter in the source code"
  (let* ((search-str "(defparameter *generation* ")
         (pos (search search-str code))
         (end-pos (position #\) code :start pos)))
    (if (and pos end-pos)
        (let* ((num-start (+ pos (length search-str)))
               (current-gen (parse-integer code :start num-start :junk-allowed t))
               (new-gen (1+ current-gen)))
          (concatenate 'string
                      (subseq code 0 num-start)
                      (write-to-string new-gen)
                      (subseq code end-pos)))
        code)))

(defun main ()
  (format t "Current generation: ~a~%" *generation*)
  (format t "Rewriting myself...~%")
  (let* ((original-code (read-self))
         (new-code (increment-generation original-code)))
    (write-self new-code)
    (format t "Done! Next generation will be: ~a~%" (1+ *generation*))))

(main)
