(define (problem hanoi5)
  (:domain hanoi)
  (:objects loc1 loc2 loc3 box1 box2 box3 box4 box5 - object)
  (:init
   (bigger loc1 box1) (bigger loc1 box2) (bigger loc1 box3) (bigger loc1 box4) (bigger loc1 box5)
   (bigger loc2 box1) (bigger loc2 box2) (bigger loc2 box3) (bigger loc2 box4) (bigger loc2 box5)
   (bigger loc3 box1) (bigger loc3 box2) (bigger loc3 box3) (bigger loc3 box4) (bigger loc3 box5)


   (clear loc2) (clear loc3) (clear box1)
   (on box5 loc1) (on box4 box5) (on box3 box4) (on box2 box3) (on box1 box2)
   (handempty)
   )
  (:goal (and (on box5 loc3) (on box4 box5) (on box3 box4) (on box2 box3) (on box1 box2)))
)