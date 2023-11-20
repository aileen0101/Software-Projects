open Bag
open Map
(** A model can predict the next word. *)
module type ModelType = sig
  type t

  val build : int -> string list -> t
  val generate_next : t -> string list -> string option
  val list_ngrams : t -> string list list
  val size : t -> int
end

(** A Map whose keys are lists of strings. *)
module String_list_map : Map.S with type key = string list = Map.Make (struct
  type t = string list

  let compare = List.compare String.compare
end)


(** Given a positive integer [n] and a list of items [l], return the list of the first n elements of l. If n is larger
than the length of l, return the empty list. *)
let rec take n lst = 
  if n<= 0 then [] else
    match lst with
    | [] -> []
    | h::t -> h :: (take (n-1) t) 
  
(** Given a positive integer [n] and a list of items [l], produce a list of all
    contiguous sublists of length [n] of the input list. If [n] is bigger than
    [l], return the empty list. Requires: [n > 0]. *)
let rec chunks (n : int) (lst : 'a list) : 'a list list = 
  if List.length lst < n then [] else
  match lst with
   | [] -> []
   | h::t-> (take n lst) :: chunks n t
 

(** Given a nonempty list [l], returns a pair consisting of the last element and
    a list of all previous elements in their original order. This should take
    O(n) time. Requires: the input list [l] is nonempty. *)
let split_last (l : 'a list) : 'a * 'a list = 
    let last_elem = List.nth (l) (List.length l - 1)  in
        let rec elem_before l last =
          match l with
          | [last] -> []
          | h::t -> h :: (elem_before t last)
          | _ -> []
    in
    (last_elem, elem_before l last_elem)

(** A model based on a sampleable bag [Bag]. *)
module BagModel (Bag : SampleBagType) : ModelType = struct
  
  module Bag : SampleBagType = Bag

  type t = {
    ng : string Bag.t String_list_map.t;
    ngram_len : int;
  }

  (**Splits each chunk of a given [chunked_corpus]. The parameter [chunked_corpus] contains the 
      corpus chunked into a certain size. *)
  let rec split_corpus =
    function
    | [] -> []
    | h::t -> split_last h :: split_corpus t

    (*Updates or initializes a bag of elements. If bag [n] is empty, initialize a bag of element m. If
       [n] is not empty, add [n] to a bag of element m.*)
    let update m n =
      let bg = (Bag.of_list [m]) in
        match n with
          | None -> Some bg
          | Some lst -> Some (Bag.join bg lst)


  (** Builds the n-gram model from a given corpus. The parameter [n] controls
      the n-gram size, and the corpus is given as a list of words [lst]. *)
  let build (n : int) (lst : string list) : t = 
   let chunked_corpus = chunks n lst in let splited_corpus
   = split_corpus chunked_corpus in 
   {ng = List.fold_left (fun accum (k,v) -> String_list_map.update v (update k) accum) String_list_map.empty (splited_corpus); 
   ngram_len = n}

   let return_ng n = n.ng

  (** Generates the next sample following a given sequence of words [input], by
      looking up the (n-1)-gram from the last [n - 1] elements of [input] in the
      map, and then sampling from the bag. *)
  let generate_next (dist : t) (input : string list) : string option =
    let there = String_list_map.mem input dist.ng in 
    match there with 
    | false -> None
    | true -> let bag = String_list_map.find input dist.ng in Bag.sample bag 

  (** Returns a list of all the keys in the n-gram model. *)
  let list_ngrams (dist : t) : string list list = 
    let all_kv = String_list_map.bindings dist.ng in
      let rec get_keys bindings = 
        match bindings with
          | [] -> []
          | h::t -> (fst h):: get_keys t
      in get_keys all_kv

  (** Returns the number of keys in the n-gram model. *)
  let size (dist : t) : int = failwith "Unimplemented"
end
(* of functor BagModel *)

(** A model that interpolates between two copies of the same model [Model], with
    different parameters [n]. *)
module InterpModel (Model : ModelType) : ModelType = struct
  (* TODO: Replace this type with your representation type. *)
  type t = unit

  (** Build an interpolated model by building two [Model]s, with parameters [n]
      and [n - 1]. *)
  let build (n : int) (lst : string list) : t = failwith "Unimplemented"

  (** Generate the next word by interpolating between the two models. If both
      models predict a word, return one of the two words at random. Otherwise if
      one of the models fails to predict a word, return the output of the other
      model. *)
  let generate_next (dist : t) (input : string list) : string option =
    failwith "Unimplemented"

  let list_ngrams (dist : t) : string list list = failwith "Unimplemented"
  let size (dist : t) : int = failwith "Unimplemented"
end
(* of module InterpModel *)
