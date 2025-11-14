#!/usr/bin/env sbcl --script
;;; A robust self-rewriting Lisp program using proper S-expression parsing
;;; This version treats code as first-class data structures, not strings

(defparameter *generation* 0)

(defun read-self-as-sexprs ()
  "Read this program's source code as a list of S-expressions"
  (with-open-file (stream "self-rewriting-robust.lisp")
    (loop for form = (read stream nil :eof)
          until (eq form :eof)
          collect form)))

(defun write-self-as-sexprs (sexprs)
  "Write S-expressions back to this file with proper formatting"
  (with-open-file (stream "self-rewriting-robust.lisp"
                          :direction :output
                          :if-exists :supersede)
    (dolist (form sexprs)
      (pprint form stream)
      (terpri stream))))

(defun find-defparameter-form (symbol sexprs)
  "Find the defparameter form for a given symbol in a list of S-expressions"
  (find-if (lambda (form)
             (and (listp form)
                  (eq (car form) 'defparameter)
                  (eq (cadr form) symbol)))
           sexprs))

(defun increment-generation-in-sexprs (sexprs)
  "Increment the *generation* value in a list of S-expressions, returning a modified copy"
  (let ((found nil))
    (let ((new-sexprs
           (mapcar (lambda (form)
                     (if (and (listp form)
                              (eq (car form) 'defparameter)
                              (eq (cadr form) '*generation*))
                         (progn
                           (setf found t)
                           `(defparameter *generation* ,(1+ (third form))))
                         form))
                   sexprs)))
      (if found
          new-sexprs
          (error "Could not find *generation* defparameter")))))

(defun verify-self-modification ()
  "Verify that the program successfully modified itself"
  (let ((original-gen *generation*))
    (format t "Current generation: ~a~%" original-gen)
    (let* ((sexprs (read-self-as-sexprs))
           (gen-form (find-defparameter-form '*generation* sexprs)))
      (if gen-form
          (let ((new-generation (third gen-form)))
            (if (= new-generation (1+ original-gen))
                (format t "✓ Self-modification successful!~%")
                (format t "✗ Self-modification failed! Expected ~a, found ~a~%"
                        (1+ original-gen) new-generation)))
          (format t "✗ Self-modification failed! Could not find *generation* defparameter in source.~%")))))

(defun transform-code-additions (sexprs)
  "Demonstrate more complex self-modification by adding new features"
  (let* ((gen-form (find-defparameter-form '*generation* sexprs))
         (current-gen (third gen-form)))
    (cond
      ;; Add execution history tracking at generation 3
      ((and (= current-gen 3)
            (not (find-defparameter-form '*execution-history* sexprs)))
       (setf sexprs (append sexprs
                            (list ';;; Added execution history tracking at generation 3
                                  '(defparameter *execution-history* '()))))
       (format t "→ Adding execution history tracking...~%"))
      ;; Add evolution function at generation 5
      ((and (= current-gen 5)
            (not (find-if (lambda (form)
                           (and (listp form)
                                (eq (car form) 'defun)
                                (eq (cadr form) 'evolve-further)))
                         sexprs)))
       (setf sexprs (append sexprs
                            (list ';;; Added evolution capability at generation 5
                                  '(defun evolve-further ()
                                     "Function added at generation 5 - demonstrates evolution"
                                     (format t "I can evolve myself in complex ways!~%")))))
       (format t "→ Adding evolution capability...~%"))
      ;; Modify behavior at generation 7
      ((= current-gen 7)
       (format t "→ Critical mass reached! Starting to exhibit emergent behavior...~%")))
    sexprs))

(defun analyze-code-structure (sexprs)
  "Analyze and report on the program's own structure"
  (let ((functions (count-if (lambda (form)
                               (and (listp form) (eq (car form) 'defun)))
                             sexprs))
        (parameters (count-if (lambda (form)
                                (and (listp form) (eq (car form) 'defparameter)))
                              sexprs))
        (total-forms (length sexprs)))
    (format t "Code structure analysis: ~D forms, ~D functions, ~D parameters~%"
            total-forms functions parameters)))

(defun main ()
  (format t "=== Robust Self-Rewriting Lisp Program ===~%")
  (format t "Current generation: ~a~%" *generation*)

  ;; Analyze current structure
  (let ((sexprs (read-self-as-sexprs)))
    (analyze-code-structure sexprs)

    ;; Demonstrate complex self-modification
    (format t "Performing self-transformation...~%")
    (setf sexprs (transform-code-additions sexprs))

    ;; Increment generation using S-expression manipulation
    (format t "Incrementing generation counter...~%")
    (setf sexprs (increment-generation-in-sexprs sexprs))

    ;; Write back as properly formatted S-expressions
    (format t "Rewriting source file...~%")
    (write-self-as-sexprs sexprs)

    ;; Verify the transformation
    (format t "Verifying self-modification...~%")
    (verify-self-modification))

  (format t "Transformation complete! Next run will be generation ~a~%" (1+ *generation*))

  ;; Call evolution function if it exists
  (when (fboundp 'evolve-further)
    (format t "Evolution capabilities detected:~%")
    (evolve-further)))

(main)