\ Model Minimize transfer cost
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xbf2376827e5dcff3
Minimize
  5 transfer_num[0,0] + 2 transfer_num[0,1] + 6 transfer_num[0,2]
   + 7 transfer_num[0,3] + 3 transfer_num[1,0] + 5 transfer_num[1,1]
   + 4 transfer_num[1,2] + 6 transfer_num[1,3] + 4 transfer_num[2,0]
   + 5 transfer_num[2,1] + 2 transfer_num[2,2] + 3 transfer_num[2,3]
Subject To
 Product_Num_constrain: transfer_num[0,0] + transfer_num[0,1]
   + transfer_num[0,2] + transfer_num[0,3] = 300
 Product_Num_constrain: transfer_num[1,0] + transfer_num[1,1]
   + transfer_num[1,2] + transfer_num[1,3] = 200
 Product_Num_constrain: transfer_num[2,0] + transfer_num[2,1]
   + transfer_num[2,2] + transfer_num[2,3] = 400
 Demand_Num_constrain: transfer_num[0,0] + transfer_num[1,0]
   + transfer_num[2,0] <= 200
 Demand_Num_constrain: transfer_num[0,1] + transfer_num[1,1]
   + transfer_num[2,1] <= 100
 Demand_Num_constrain: transfer_num[0,2] + transfer_num[1,2]
   + transfer_num[2,2] <= 450
 Demand_Num_constrain: transfer_num[0,3] + transfer_num[1,3]
   + transfer_num[2,3] <= 250
Bounds
 30 <= transfer_num[0,0] <= 500
 30 <= transfer_num[0,1] <= 500
 30 <= transfer_num[0,2] <= 500
 30 <= transfer_num[0,3] <= 500
 30 <= transfer_num[1,0] <= 500
 30 <= transfer_num[1,1] <= 500
 30 <= transfer_num[1,2] <= 500
 30 <= transfer_num[1,3] <= 500
 30 <= transfer_num[2,0] <= 500
 30 <= transfer_num[2,1] <= 500
 30 <= transfer_num[2,2] <= 500
 30 <= transfer_num[2,3] <= 500
Generals
 transfer_num[0,0] transfer_num[0,1] transfer_num[0,2] transfer_num[0,3]
 transfer_num[1,0] transfer_num[1,1] transfer_num[1,2] transfer_num[1,3]
 transfer_num[2,0] transfer_num[2,1] transfer_num[2,2] transfer_num[2,3]
End
