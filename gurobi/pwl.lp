\ Model pwl_demo
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x75bdb95151b30ffb
Maximize
  0 x + y
Subject To
Bounds
 x <= 5
General Constraints
 pwl_constraint: y = PWL ( x ) : (0, 1) (2, 5) (5, 2)
End
