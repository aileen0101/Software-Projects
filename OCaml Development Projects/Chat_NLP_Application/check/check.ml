(* DO NOT EDIT THIS FILE *)

open Chat

module type T = sig
  val hours_worked : int
end

module M : T = Author

let _ = if M.hours_worked < 0 then exit 1