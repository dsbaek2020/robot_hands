# 이 파일은 진해 여자고등학교 학생들의 작품입니다.
# 저작자: 진해여고
# 코드작성 지도: 백대성 
# 내용: 라즈베리 파이 컴퓨터와 레고 모터/ 힘 센서를 이용한 로봇 의수의 손부분 기능을 구현한 파일

# 상세 설명: 
#       이 파이썬 코드에서는 사용자가 힘센서를 누를때 의도하지 않는 떨림이 발생한 경우가 있으면 ,
#       의수의 손부분이 진동하지 않도록 하는 안정화 제어 알고리즘을 구현하는 문제해결 아이디어를 고민하고 만들어내었다. 이를 통해서
#       사용자는 의수의 손부분을 떨지 안도록 쉽게 사용할 수 있고, 편의성을 높이게 될것으로 기대된다. 


#       진해여고 학생들의 문제해결 아이디어를 구현하기 쉽게 코드화한  코딩한 기법과 배경이론 :  "유한 상태머신" 및 "수치 미분" 을 적용함

# 더 고칠 부분:
#       각 상태에서 다음 상태롤 전환 하기 위한 물리적 값과 논리적 값을 기준을 실험하면서 재정의, 그리고 알고리즘의 부족한 부분을 검토

# 2023. 12.12(화)

from buildhat import ForceSensor, Motor
import time


#함수 정의:
#함수 이름:  decision_next_state
#함수의 설명 : 이 함수는 로봇의수의 힘센서와 손부분 모터의 연동 동작의 상태를 정의하고, 힘센서값, 힘센서의 변화(기울기)
#           등을 고려하여, 힘센서-모터간 연동 동작을 어떻게 할지 상태를 3개로 분류하고 정의하는 함수입니다.

        #----상태정의---------------------------------------------------------------------
        # reday : 준비 상태이며, 손 부분 모터를 펼침으로 작동하는 상태임
        #          힘센서의 값이 0보다 커지면 working 상태로 전환한다. 

        # working : 물체을 잡는 손의 펼침과 닫힘 간격을  힘 센서의 값의 함수로 작동하는 상태이다.
        #           힘센서와 동기화 되어 작동하는 모션이된 상태이다. 
        #           만약 힘 센서의 값의 변화량이  0.5초 이상 10%이하로 된다면 홀딩 상태로 전환 한다.


        # holding : 사용자의 힘센서 잡는 수치가 20%이하라면 마지막 working상태를 유지한다.
        #           만약 힘 센서의 값 변화량이 0.5초이상 20% 이상 이라면 ready 상태로 전환한다.   
        #--------------------------------------------------------------------------------

        #-----------------상태 천이 정의 ------------------------------
        #현재 상태:  ready(완전 펼침)    holding(마지막 working 상태유지)  working(힘센서 값에 의해서 순시적으로 작동)
        #다음 상태 : working           reday                           holding
        #------------------------------------------------------------

def decision_next_state(switchForce, current_state, forceChangeValue):
  #현재 상태가 물체를 잡기전 준비 상태이며, 힘센서의 값이 0보다 커지면
  #다음 상태를 잡기상태(woriking)으로 전환한다.
  if current_state == 'ready'  and switchForce > 0:
    next_state = 'working'
    
  #현재의 상태가 물체를 잡은 상태이며, 힘조절 센서값의 변화가 5%이하라면
  #다음 상태를 홀딩(물체를 계속 잡아주는 상태)으로 전환한다.
  elif current_state == 'working':
    if abs(forceChangeValue) < 10:
       next_state = 'holding'
    else:
       next_state = 'working' 
    
  #현재 상태가 홀딩(사용자의 힘센서 누름이 20% 이하로 변화가 있더라도 유지)이라며
  # 이때 힘센서의 수치 변화가 20%이상이 되면 사용자가 놓기를 원하는 의도로 파악하여
  # 다음 상태를 준비 상태로 전환한다. 
  elif current_state == 'holding' and  abs(forceChangeValue) > 20:
    next_state = 'ready'

  #위의 모든 조건식에 만족하는 상태가 아니라면 다음 상태는 현재 상태와 같도록 유지한다. 
  else:
    next_state = current_state

  return next_state



def linear_hands_control(force):

        #모터의 위치(각도)를 힘센서 값에 따라서 선형적으로 변화하는 1차 함수로 계산한다. 
        hand_motor_angle = round(force/100*90)
        
        #위에서 계산된 위치로 이동 되도록 모터를 회전 시킨다. 
        myHands.run_to_position(hand_motor_angle)
        
        
        #실제 모터의 위치값을 수신받아 터미널에 출력한다. 
        real_angle = myHands.get_aposition()
        print("각도[명령] :", hand_motor_angle, "각도[응답] :", real_angle)
        
        return real_angle 


#전역 변수 및 객체 정의

#모터 객체 선언
myHands = Motor('B')
# 힘센서 객체 선언 
s1 = ForceSensor('A')
#상태 변수 선언 
state = "ready"

#미분 주기 정의                      단위 [sec]
T_of_differenciation = 0.5         
#힘센서 미분값(3초 간격으로 미분) 정의   단위 [%]/sec
diffent_of_forceSensor =0
#현재 힘 센서량 및 과거 0.5초전 힘 센서량, 단위 [%]
current_force = 0
pre_force = 0

#최대 펼침시 손 부분 모터의 각도 
extending_angle_of_hands = 0       #단위 [도]

#working 상태의 마지막 각도 저장 변수 
last_angle_at_working = 0

#--메인 루틴 시작 -----------------------------------------------
while True:
   current_force = s1.get_force()
   print('힘 센서 값[N] = ', current_force)
   
   #미분량 구하기
   diffent_of_forceSensor = current_force - pre_force
   
   #상태 결정 함수를 호출한다. 호출시 현재의 힘센서 량, 현재 상태, 힘센서의 변화율(미분)을 인수로 입력한다. 
   state = decision_next_state(current_force,
                               state,
                               diffent_of_forceSensor)
   

   if state == 'working':
        print('현재 상태: 힘센서와 동기화되어 작동(working)')
        last_angle_at_working = linear_hands_control(current_force)
    
   elif state == 'holding':
        print('현재 상태: 잡기 유지(holding)')
        myHands.run_to_position(last_angle_at_working) #working에서의 마지막 각도를 유지하기 위해서, 그각도로 이동함

        
   elif state == 'ready':
        print('현재 상태: 대기 상태(ready)')
        linear_hands_control(current_force)
        #myHands.run_to_position(extending_angle_of_hands)
   else:
        print('오류 발생: 상태를 정의할 수 없는 오류에 빠짐')
        


   time.sleep(T_of_differenciation) #미분 주기를 위해서 컴퓨터를 슬립 시킨다. 
   #과거 힘 센서의 값을 저장한다. 
   pre_force = current_force







#--아이디어를 핵심이 담긴--래거시 코드 -----------------------------

'''
while True:
  F1 = s1.get_force()
  print('힘 센서 값[N] = ', F1)
  
  if F1!=0 and co != "waiting" :
    angle = F1/100*90
    angle = round(angle)
    NyHands.run_to_position(angle)
    print("각도 :", angle)

    time.sleep(3)
    F2 = s1.get_force()

    diff = F1 - F2

  elif F1 != 0 and co == "waiting" :
    time.sleep(3)
    F2 = s1.get_force()

    diff = F1 - F2

  if -5 <= diff <= 5:
    co = "waiting"
    time.sleep(3)

  elif diff<-5 or diff>5 : 
    co = "working"
    
'''
