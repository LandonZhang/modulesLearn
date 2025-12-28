\ Model indicator_overloaded
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xa5fb035bbc3ef503
Maximize
  x + y + 0 flag
Subject To
 indicator_constr: flag = 1 -> x + y <= 5
Bounds
 x <= 10
 y <= 10
Binaries
 flag
End
