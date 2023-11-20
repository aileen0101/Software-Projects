open OUnit2
open Chat
open Ngrams
open Model
open Bag

(********************************************************************
   Here are some helper functions for your testing of bag-like lists.
 ********************************************************************)

(** [cmp_bag_like_lists lst1 lst2] compares two lists to see whether they are
    equivalent bag-like lists. That means checking that they they contain the
    same elements with the same number of repetitions, though not necessarily in
    the same order. *)
let cmp_bag_like_lists lst1 lst2 =
  let sort1 = List.sort compare lst1 in
  let sort2 = List.sort compare lst2 in
  sort1 = sort2

(** [pp_string s] pretty-prints string [s]. *)
let pp_string s = "\"" ^ s ^ "\""

(** [pp_list pp_elt lst] pretty-prints list [lst], using [pp_elt] to
    pretty-print each element of [lst]. *)
let pp_list pp_elt lst =
  let pp_elts lst =
    let rec loop n acc = function
      | [] -> acc
      | [ h ] -> acc ^ pp_elt h
      | h1 :: (h2 :: t as t') ->
          if n = 100 then acc ^ "..." (* stop printing long list *)
          else loop (n + 1) (acc ^ pp_elt h1 ^ "; ") t'
    in
    loop 0 "" lst
  in
  "[" ^ pp_elts lst ^ "]"


(* These tests demonstrate how to use [cmp_bag_like_lists] and [pp_list] to get
   helpful output from OUnit. *)
let cmp_demo =
  [
    ( "order is irrelevant" >:: fun _ ->
      assert_equal ~cmp:cmp_bag_like_lists ~printer:(pp_list pp_string)
      [ "foo"; "bar" ] [ "bar"; "foo" ] );
    (* Uncomment this test to see what happens when a test case fails.
      ( "counts must be the same" >:: fun _ -> assert_equal
       ~cmp:cmp_bag_like_lists ~printer:(pp_list pp_string) ["foo"; "foo"]
      ["foo"]); *)
  ]

(********************************************************************
   End helper functions.
 ********************************************************************)

(* Bags with random sampling. *)
module Test_RandBag = Bag.RandomBag

(* Here are some examples of how to create bags. *)

let empty_bag = Test_RandBag.of_list [] 
let b1 = Test_RandBag.of_list [ "1" ] 
let b2 = Test_RandBag.of_list [ "1"; "2"; "3" ]

let b22 = Test_RandBag.of_list["2";"1"; "3"]
let b_dup = Test_RandBag.of_list ["2" ; "2"; "2"; "2"]

module Test_FreqBag = Bag.FrequencyBag

let f_empty_bag = Test_FreqBag.of_list []
let f_b1 = Test_FreqBag.of_list ["1"]
let f_b2 = Test_FreqBag.of_list ["1"; "1"; "2"; "2"; "3"]
let f_b22 = Test_FreqBag.of_list ["1"; "1"; "1" ;"2"; "2"; "2" ;"3"; "3"; "3"]
let f_b3 = Test_FreqBag.of_list ["1"; "2"; "3"]
let f_b4 = Test_FreqBag.of_list ["1"; "1"; "1"; "1"]
let f_b5 = Test_FreqBag.of_list ["1"; "2"; "4"; "5"; "5"]


(* Next-word model based on random sampling bag. *)
module Test_RandModel = Model.BagModel (Test_RandBag)

(* Here are some examples of how to create next-word models. *)
let dist = 
Test_RandModel.build 1 [ "1"; "2"; "3"; "4"; "4"; "4"; "2"; "2"; "3"; "1" ]

let dist2 =
  Test_RandModel.build 3 [ "1"; "2"; "3"; "4"; "4"; "4"; "2"; "2"; "1" ]

let dist3 =
    Test_RandModel.build 5 [ "1"; "2"; "3"; "4"]
  
let dist4 =
    Test_RandModel.build 5 []
  
let dist5 =
  Test_RandModel.build 3 [ "1"; "2"; "3"; "4"]


(*Next-word models based on frequency sampling bag*)
module Test_FreqModel = Model.BagModel(Test_FreqBag)
let f_mod = Test_FreqModel.build 3 ["1"; "1"; "1" ;"2"; "2"; "2" ;"3"; "3"; "3"]
let f_mod_exp = let d = String_list_map.empty in 
let e = String_list_map.add ["1"; "1"] (Test_FreqBag.of_list ["1";"2"]) d in let f =String_list_map.add ["1"; "2"] (Test_FreqBag.of_list ["2"]) e
in let g = String_list_map.add ["2"; "2"] (Test_FreqBag.of_list ["2"; "3"]) f in
let h = String_list_map.add ["2"; "3"] (Test_FreqBag.of_list ["3"]) g in 
String_list_map.add ["3"; "3"] (Test_FreqBag.of_list ["3"]) h

let f_mod2 = Test_FreqModel.build 2 ["1"; "2"; "4"; "5"; "5"]
let f_mod2_exp = let d = String_list_map.empty in 
let e = String_list_map.add ["1"] (Test_FreqBag.of_list ["2"]) d in let f =String_list_map.add [ "2"] (Test_FreqBag.of_list ["4"]) e
in let g = String_list_map.add ["4"] (Test_FreqBag.of_list ["5"]) f in
 String_list_map.add ["5"] (Test_FreqBag.of_list ["5"]) g 

let f_mod3 = Test_FreqModel.build 3 ["1"; "1"; "2"; "1"; "1"; "2" ;"3"; "2"; "3"; "4"]
let f_mod3_exp =let d = String_list_map.empty in 
let e = String_list_map.add ["1"; "1"] (Test_FreqBag.of_list ["2";"2"]) d in let f =String_list_map.add ["1"; "2"] (Test_FreqBag.of_list ["1"; "3"]) e
in let g = String_list_map.add ["2"; "1"] (Test_FreqBag.of_list ["1"]) f in
let h = String_list_map.add ["2"; "3"] (Test_FreqBag.of_list ["2"; "4"]) g in 
String_list_map.add ["3"; "2"] (Test_FreqBag.of_list ["3"]) h

module Test_Ngram = Ngram(Test_FreqModel)
let d1 = Test_Ngram.build 3 ["1"; "1"; "2"; "1"; "1"; "2" ;"3"; "2"; "3"; "4"]

(* TODO: add unit tests for modules below. You are free to reorganize the
   definitions below. Just keep it clear which tests are for which modules. *)

let bag_tests = [
(*RandomBag Tests*)
(*Testing to_list*)
("to_list empty bag" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) ([]) (Bag.RandomBag.to_list empty_bag));
("to_list bag with one element" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"]) (Bag.RandomBag.to_list b1));
("to_list bag with duplicate elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["2"; "2"; "2"; "2"]) (Bag.RandomBag.to_list b_dup));
("to_list bag with multiple elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "2"; "3"]) (Bag.RandomBag.to_list b2));

(*Testing of_list*)
("of_list empty bag" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) ([]) (Bag.RandomBag.to_list (Bag.RandomBag.of_list [])));
("of_list bag with one element" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["9"]) (Bag.RandomBag.to_list (Bag.RandomBag.of_list ["9"])));
("of_list bag with multiple elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["5"; "7"; "10"; "11"]) (Bag.RandomBag.to_list (Bag.RandomBag.of_list ["5"; "7"; "10"; "11"])));

(*Testing join*)
("join joining empty bags" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) ([]) (Bag.RandomBag.to_list ((Bag.RandomBag.join empty_bag empty_bag))));
("join joining empty bag with bag of one element" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"]) (Bag.RandomBag.to_list ((Bag.RandomBag.join empty_bag b1))));
("join joining two bags each with multiple elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "2"; "3"; "2"; "1"; "3"]) (Bag.RandomBag.to_list ((Bag.RandomBag.join b2 b22))));
("join joining empty bag with bag of multiple elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["2"; "1"; "3"]) (Bag.RandomBag.to_list ((Bag.RandomBag.join empty_bag b22))));
("join joining  bag of single element and bag of multiple elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "2"; "3"]) (Bag.RandomBag.to_list ((Bag.RandomBag.join b1 b2))));

(*FrequencyBag Tests*)
(*Testing to_list*)
("to_list empty bag" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) ([]) (Bag.FrequencyBag.to_list f_empty_bag));
("to_list bag with one element" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"]) (Bag.FrequencyBag.to_list f_b1));
("to_list bag with at least 2 elements with same highest multiplicity" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "2"; "2"; "3"]) (Bag.FrequencyBag.to_list f_b2));
("to_list bag with same multiplicity for all elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1" ;"2"; "2"; "2" ;"3"; "3"; "3"]) (Bag.FrequencyBag.to_list f_b22));
("to_list bag with all the same elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1"; "1"]) (Bag.FrequencyBag.to_list f_b4));

(*Testing of_list*)
("of_list empty bag" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) ([]) (Bag.FrequencyBag.to_list (Bag.FrequencyBag.of_list [])));
("of_list bag with one element" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["9"]) (Bag.FrequencyBag.to_list (Bag.FrequencyBag.of_list ["9"])));
("of_list bag with at least 2 elements with same highest multiplicity" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "2"; "2"; "3"]) (Bag.FrequencyBag.to_list (Bag.FrequencyBag.of_list ["1"; "1"; "2"; "2"; "3"])));
("of_list bag with same multiplicity for all elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1" ;"2"; "2"; "2" ;"3"; "3"; "3"]) (Bag.FrequencyBag.to_list (Bag.FrequencyBag.of_list ["1"; "1"; "1" ;"2"; "2"; "2" ;"3"; "3"; "3"])));
("of_list bag with all the same elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1"; "1"]) (Bag.FrequencyBag.to_list (Bag.FrequencyBag.of_list ["1"; "1"; "1"; "1"])));

(*Testing join*)
("join joining empty bags" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) ([]) (Bag.FrequencyBag.to_list ((Bag.FrequencyBag.join f_empty_bag f_empty_bag))));
("join joining empty bag with bag of one element" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"]) (Bag.FrequencyBag.to_list ((Bag.FrequencyBag.join f_empty_bag f_b1))));
("join joining empty bag with bag of multiple elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1" ;"2"; "2"; "2" ;"3"; "3"; "3"]) (Bag.FrequencyBag.to_list ((Bag.FrequencyBag.join f_empty_bag f_b22))));
("join joining two bags of multiple elements - overlapping elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1" ; "1" ;"1"; "2"; "2"; "2" ;"2"; "2"; "3";"3"; "3"; "3"]) (Bag.FrequencyBag.to_list ((Bag.FrequencyBag.join f_b2 f_b22))));
("join joining another two bags of multiple elements - overlapping elements" >:: fun _ -> assert_equal ~cmp: cmp_bag_like_lists ~printer: (pp_list pp_string) (["1"; "1"; "1"; "2"; "2"; "2"; "3";"4"; "5"; "5"]) (Bag.FrequencyBag.to_list ((Bag.FrequencyBag.join f_b2 f_b5))));

(*Testing sample*)

("sample of empty bag" >:: fun _ -> assert_equal (None) ((Bag.FrequencyBag.sample f_empty_bag)));
("sample of bag of one element" >:: fun _ ->  assert_equal (Some "1") ((Bag.FrequencyBag.sample f_b1)));
("sample of bag with at least 2 elements with same highest multiplicity">:: fun _ ->  assert_equal (Some "1") ((Bag.FrequencyBag.sample f_b2)));
("sample of bag with same multiplicity for all elements" >:: fun _ ->  assert_equal (Some "1") ((Bag.FrequencyBag.sample f_b22)));
("sample of bag with all the same elements" >:: fun _ ->  assert_equal (Some "1") ((Bag.FrequencyBag.sample f_b4)));
]

let model_tests = [
(*Testing chunks function*)
("chunks sublisting an empty list" >:: fun _ -> assert_equal ([]) (chunks 3 []));
("chunks sublisting a list of one element with length 1" >:: fun _ -> assert_equal ([["1"]]) (chunks 1 ["1"]));
("chunks sublisting a list of 4 elements with length 3" >:: fun _ -> assert_equal ([["1"; "3"; "4"]; ["3"; "4"; "5"]]) (chunks 3 ["1"; "3"; "4"; "5"]));
("chunks sublisting a list of 2 elements with length 3" >:: fun _ -> assert_equal ([]) (chunks 3 ["3; 5"]));
("chunks sublisting a list of 6 elements with length 1" >:: fun _ -> assert_equal ([["1"]; ["3"]; ["4"]; ["5"]; ["6"]; ["7"]]) (chunks 1 ["1"; "3"; "4"; "5"; "6"; "7"]));
("chunks sublisting a list of 6 elements with length 6" >:: fun _ -> assert_equal ([["1"; "3"; "4"; "5"; "6"; "7"]]) (chunks 6 ["1"; "3"; "4"; "5"; "6"; "7"]));
("chunks sublisting a list of 4 elements with length 2" >:: fun _ -> assert_equal ([["1"; "3"]; ["3"; "4"]; ["4"; "5"]]) (chunks 2 ["1"; "3"; "4"; "5"]));

(*Testing split_last function*)
("split_last split list of size 1" >:: fun _ -> assert_equal (1, []) (split_last [1]));
("split_last split list of size 2" >:: fun _ -> assert_equal (2, [1]) (split_last [1; 2]));
("split_last split list of size 5" >:: fun _ -> assert_equal (6, [1; 2; 3; 5]) (split_last [1; 2; 3; 5; 6]));
("split_last split list of size 10" >:: fun _ -> assert_equal (302, [1; 2; 3; 5; 6; 7; 8; 11; 45]) (split_last [1; 2; 3; 5; 6; 7; 8; 11; 45; 302]));

(*Testing build function*)
(*("build example 1" >:: fun _ -> assert_equal (f_mod_exp) (Test_FreqModel.return_ng (f_mod)));*)
(*("build example 2" >:: fun _ -> assert_equal (f_mod2_exp) (f_mod2.ng));
("build example 3" >:: fun _ -> assert_equal (f_mod3_exp) (f_mod3.ng));*)

(*Testing generate_next*)
("generate_next example 1" >:: fun _ -> assert_equal (Some "2") (Test_FreqModel.generate_next (f_mod) ["1"; "1"]));
("generate_next example 2" >:: fun _ -> assert_equal (Some "2") (Test_FreqModel.generate_next (f_mod2) ["1"]));
("generate_next example 3" >:: fun _ -> assert_equal (Some "2") (Test_FreqModel.generate_next (f_mod3) ["1"; "1"]));

(*Testing list_ngrams*)
("list_ngrams split n gram for dist" >:: fun _ -> assert_equal ([[]]) (Test_RandModel.list_ngrams dist));
("list_ngrams split n gram for dist2" >:: fun _ -> assert_equal ~printer: (pp_list (pp_list pp_string))  ([["1"; "2"]; ["2"; "2"]; ["2"; "3"]; ["3"; "4"]; ["4"; "2"]; ["4"; "4"]]) (Test_RandModel.list_ngrams dist2));
("list_ngrams split n gram for dist3" >:: fun _ -> assert_equal ([]) (Test_RandModel.list_ngrams dist3));
("list_ngrams split n gram for dist4" >:: fun _ -> assert_equal ([]) (Test_RandModel.list_ngrams dist4));
("list_ngrams split n gram for dist5" >:: fun _ -> assert_equal  ~printer: (pp_list (pp_list pp_string)) ([["1"; "2"]; ["2"; "3"]]) (Test_RandModel.list_ngrams dist5));

]

let ngram_tests = [
(*Testing sample_sequence*)
("sample_sequence example 1" >:: fun _ -> assert_equal (["2"; "3"; "4"]) (Test_Ngram.sample_sequence (d1) 3 ["1"; "1"]));
("sample_sequence example 2" >:: fun _ -> assert_equal (["1";"2"]) (Test_Ngram.sample_sequence (d1) 2 ["2"; "1"]));
("sample_sequence example 3" >:: fun _ -> assert_equal ~printer: (pp_list pp_string) (["3"; "4"]) (Test_Ngram.sample_sequence (d1) 2 ["1"; "2"]));

]

let suite =
  "test suite for A2"
  >::: List.flatten [ cmp_demo; bag_tests; model_tests; ngram_tests ]

let () = run_test_tt_main suite
