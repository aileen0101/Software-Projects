(** The signature of sampleable bags (multisets). *)
module type SampleBagType = sig
  type 'a t

  val to_list : 'a t -> 'a list
  val of_list : 'a list -> 'a t
  val join : 'a t -> 'a t -> 'a t
  val sample : 'a t -> 'a option
end

(** Sampleable bag such that sample returns elements with probability
    proportional to their multiplicity. *)
module RandomBag : SampleBagType = struct
  type 'a t = 'a list

  let to_list (b : 'a t) : 'a list = b
  let of_list (lst : 'a list) : 'a t = lst
  let join (b1 : 'a t) (b2 : 'a t) : 'a t = b1 @ b2
  let sample (b : 'a t) : 'a option = 
    match b with
    | [] -> None
    | h -> let len = List.length (to_list b) in 
    let rand_num = Random.int len in 
    let elem = List.nth (to_list b) (rand_num) in Some elem
  end

(** Sampleable bag such that sample always returns the element of highest
    multiplicity. Ties are broken arbitrarily. *)
module FrequencyBag : SampleBagType = struct
  type 'a t = ('a * int) list

(*Compares two pairs [kv1] and [kv2], returning the pair
with the larger integer value. The parameters [kv1] and [kv2] are
   a pair consisting of an element as its first
   element and an integer as its second element. Returns 0 if
    the integers of both pairs are equal, 1 if the integer of the
  first pair is greater than that of the second, and -1 if the integer
  of the first pair is less than that of the second*)
let compare_pairs kv1 kv2 = 
   let int1 = (snd kv1) in let int2 = (snd kv2) in compare int1 int2

(**Updates the frequency of element [e] for list of pairs [p] and sorts
the list by frequency after updating. The parameter [p] 
contains a list of pairs where the first element 
is the bag element and second element is its current frequency.*)
let freq_update p e =
  let new_p = 
    match List.assoc_opt e p with
      | Some vl -> (e, vl + 1) :: List.remove_assoc e p
      | None -> (e, 1) :: p
  in new_p

(**Given a pair [p1] of an element and an integer, convert the pair
into a list of that element enumerated by the number of times specified
by the integer element in the pair. Example: enum ("3",3) would return ["3"; "3"; "3"].*)
  let rec enum p1 = 
    match p1 with
      |(hd, t1) -> if t1 = 1 then [hd] else hd :: enum (hd, t1-1)

  let rec to_list (b : 'a t) : 'a list = 
    match b with
    | [] -> []
    | h::t -> enum h @ to_list t
    
  let of_list (lst : 'a list) : 'a t = List.sort compare_pairs (List.fold_left freq_update [] lst)


  let rec join (b1 : 'a t) (b2 : 'a t) : 'a t =
    let b1_list = to_list b1 in let b2_list = to_list b2 
  in let comb_list = b1_list @ b2_list in let new_bag = of_list comb_list
in new_bag

  let sample (b : 'a t) : 'a option = 
  let last = (List.length b-1) in match b with
    | [] -> None
    | lst -> Some (fst (List.nth b last))
end
