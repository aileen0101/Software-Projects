(** The signature of sampleable bags (multisets). *)
module type SampleBagType = sig

  (** Type representing the data in the bag. *)
  type 'a t

  (** Convert a sampleable bag to a list of items. *)
  val to_list : 'a t -> 'a list

  (** Convert a list of items into a sampleable bag. *)
  val of_list : 'a list -> 'a t

  (** Combine two sampleable bags. The multiplicity of an item in the output bag
      is the sum of the multiplicities of the item in the two input bags. *)
  val join : 'a t -> 'a t -> 'a t

  (** Draw an item from the sampleable bag. Return [None] if the bag is empty. *)
  val sample : 'a t -> 'a option
end

(** Sampleable bag such that sample returns elements with probability
    proportional to their multiplicity. *)
module RandomBag : SampleBagType

(** Sampleable bag such that sample always returns the element of highest
    multiplicity. Ties are broken arbitrarily. *)
module FrequencyBag : SampleBagType
