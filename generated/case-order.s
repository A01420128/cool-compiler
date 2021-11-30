
    .data
    .align  2
    .globl  class_nameTab
    .globl  Main_protObj
    .globl  Int_protObj
    .globl  String_protObj
    .globl  bool_const0
    .globl  bool_const1
    .globl  _int_tag
    .globl  _bool_tag
    .globl  _string_tag

_int_tag:
    .word   2
_bool_tag:
    .word   3
_string_tag:
    .word   4

    .globl  _MemMgr_INITIALIZER
_MemMgr_INITIALIZER:
    .word   _NoGC_Init
    .globl  _MemMgr_COLLECTOR
_MemMgr_COLLECTOR:
    .word   _NoGC_Collect
    .globl  _MemMgr_TEST
_MemMgr_TEST:
    .word   0

    .word   -1
str_const9:
    .word   4
    .word   6
    .word   String_dispTab
    .word   int_const1
    .ascii  "Object"
    .byte   0
    .align  2

    .word   -1
str_const8:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const2
    .ascii  "IO"
    .byte   0
    .align  2

    .word   -1
str_const7:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const3
    .ascii  "Int"
    .byte   0
    .align  2

    .word   -1
str_const6:
    .word   4
    .word   6
    .word   String_dispTab
    .word   int_const4
    .ascii  "Bool"
    .byte   0
    .align  2

    .word   -1
str_const5:
    .word   4
    .word   6
    .word   String_dispTab
    .word   int_const1
    .ascii  "String"
    .byte   0
    .align  2

    .word   -1
str_const4:
    .word   4
    .word   6
    .word   String_dispTab
    .word   int_const4
    .ascii  "Main"
    .byte   0
    .align  2

    .word   -1
str_const3:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const0
    .byte   0
    .align  2

    .word   -1
str_const2:
    .word   4
    .word   8
    .word   String_dispTab
    .word   int_const5
    .ascii  "--filename--"
    .byte   0
    .align  2

    .word   -1
str_const1:
    .word   4
    .word   6
    .word   String_dispTab
    .word   int_const1
    .ascii  "main\n"
    .byte   0
    .align  2

    .word   -1
str_const0:
    .word   4
    .word   7
    .word   String_dispTab
    .word   int_const6
    .ascii  "object\n"
    .byte   0
    .align  2

    .word   -1
int_const0:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   0

    .word   -1
int_const1:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   6

    .word   -1
int_const2:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   2

    .word   -1
int_const3:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   3

    .word   -1
int_const4:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   4

    .word   -1
int_const5:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   12

    .word   -1
int_const6:
    .word   2
    .word   4
    .word   Int_dispTab
    .word   8

    .word   -1
bool_const0:
    .word   3
    .word   4
    .word   Bool_dispTab
    .word   0
    .word   -1
bool_const1:
    .word   3
    .word   4
    .word   Bool_dispTab
    .word   1
class_nameTab:
    .word    str_const9
    .word    str_const8
    .word    str_const7
    .word    str_const6
    .word    str_const5
    .word    str_const4
class_objTab:
    .word    Object_protObj
    .word    Object_init
    .word    IO_protObj
    .word    IO_init
    .word    Int_protObj
    .word    Int_init
    .word    Bool_protObj
    .word    Bool_init
    .word    String_protObj
    .word    String_init
    .word    Main_protObj
    .word    Main_init
Object_dispTab:
    .word    Object.abort
    .word    Object.type_name
    .word    Object.copy
IO_dispTab:
    .word    Object.abort
    .word    Object.type_name
    .word    Object.copy
    .word    IO.out_string
    .word    IO.out_int
    .word    IO.in_string
    .word    IO.in_int
Int_dispTab:
    .word    Object.abort
    .word    Object.type_name
    .word    Object.copy
Bool_dispTab:
    .word    Object.abort
    .word    Object.type_name
    .word    Object.copy
String_dispTab:
    .word    Object.abort
    .word    Object.type_name
    .word    Object.copy
    .word    String.length
    .word    String.concat
    .word    String.substr
Main_dispTab:
    .word    Object.abort
    .word    Object.type_name
    .word    Object.copy
    .word    IO.out_string
    .word    IO.out_int
    .word    IO.in_string
    .word    IO.in_int
    .word    Main.main
    .word    -1
Object_protObj:
    .word    0
    .word    3
    .word    Object_dispTab
    .word    -1
IO_protObj:
    .word    1
    .word    3
    .word    IO_dispTab
    .word    -1
Int_protObj:
    .word    2
    .word    4
    .word    Int_dispTab
    .word    int_const0
    .word    -1
Bool_protObj:
    .word    3
    .word    4
    .word    Bool_dispTab
    .word    int_const0
    .word    -1
String_protObj:
    .word    4
    .word    5
    .word    String_dispTab
    .word    int_const0
    .word    0
    .word    -1
Main_protObj:
    .word    5
    .word    3
    .word    Main_dispTab

   .globl  heap_start 
heap_start:
    .word   0 

    .text    
    .globl  Main_init 
    .globl  Int_init 
    .globl  String_init 
    .globl  Bool_init 
    .globl  Main.main 
Object_init:
    addiu	$sp $sp -12 
    sw	$fp 12($sp) 
    sw	$s0 8($sp) 
    sw	$ra 4($sp) 
    addiu	$fp $sp 4 
    move	$s0 $a0 
    move	$a0 $s0 
    lw	$fp 12($sp) 
    lw	$s0 8($sp) 
    lw	$ra 4($sp) 
    addiu	$sp $sp 12 
    jr	$ra 
IO_init:
    addiu	$sp $sp -12 
    sw	$fp 12($sp) 
    sw	$s0 8($sp) 
    sw	$ra 4($sp) 
    addiu	$fp $sp 4 
    move	$s0 $a0 
    jal Object_init
    move	$a0 $s0 
    lw	$fp 12($sp) 
    lw	$s0 8($sp) 
    lw	$ra 4($sp) 
    addiu	$sp $sp 12 
    jr	$ra 
Int_init:
    addiu	$sp $sp -12 
    sw	$fp 12($sp) 
    sw	$s0 8($sp) 
    sw	$ra 4($sp) 
    addiu	$fp $sp 4 
    move	$s0 $a0 
    jal Object_init
    move	$a0 $s0 
    lw	$fp 12($sp) 
    lw	$s0 8($sp) 
    lw	$ra 4($sp) 
    addiu	$sp $sp 12 
    jr	$ra 
Bool_init:
    addiu	$sp $sp -12 
    sw	$fp 12($sp) 
    sw	$s0 8($sp) 
    sw	$ra 4($sp) 
    addiu	$fp $sp 4 
    move	$s0 $a0 
    jal Object_init
    move	$a0 $s0 
    lw	$fp 12($sp) 
    lw	$s0 8($sp) 
    lw	$ra 4($sp) 
    addiu	$sp $sp 12 
    jr	$ra 
String_init:
    addiu	$sp $sp -12 
    sw	$fp 12($sp) 
    sw	$s0 8($sp) 
    sw	$ra 4($sp) 
    addiu	$fp $sp 4 
    move	$s0 $a0 
    jal Object_init
    move	$a0 $s0 
    lw	$fp 12($sp) 
    lw	$s0 8($sp) 
    lw	$ra 4($sp) 
    addiu	$sp $sp 12 
    jr	$ra 
Main_init:
    addiu	$sp $sp -12 
    sw	$fp 12($sp) 
    sw	$s0 8($sp) 
    sw	$ra 4($sp) 
    addiu	$fp $sp 4 
    move	$s0 $a0 
    jal IO_init
    move	$a0 $s0 
    lw	$fp 12($sp) 
    lw	$s0 8($sp) 
    lw	$ra 4($sp) 
    addiu	$sp $sp 12 
    jr	$ra 

Main.main:
    addiu   $sp    $sp    -24        #inm: frame has 3 locals
    sw      $fp    24($sp)         #inm: save $fp
    sw      $s0    20($sp)         #inm: save $s0 (self)
    sw      $ra    16($sp)         #inm: save $ra
    addiu   $fp    $sp    4           #inm: $fp points to locals
    move    $s0    $a0                #inm: self to $s0

    
    move    $a0     $s0                 #self

    sw      $a0     0($fp)            #letdecl: initial value of thing

    
    lw      $a0     0($fp)            #obj: load [thing], Object

    bne     $a0    $zero  label2      #case: protect from case on void (abort)
    la      $a0    str_const0              #case: fileName
    li      $t1    9                   #case: line number
    jal    _case_abort2
label2:
    lw      $t1    0($a0)                 #case: load obj tag

    blt     $t1    5   label4    #case: 5, Main
    bgt     $t1    5   label4    #case: 5, Main
    sw      $a0    28($fp)                #case: m

    la      $a0     str_const1           #literal, main\n

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label1      #call: protect from dispatch to void
    la      $a0    str_const2               #call: constant object with name of the file
    li      $t1    11                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label1:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    12($t1)              #call: method out_string is at offset 12
    jalr    $t1

    b       label3                       #case: go to end
label4:

    blt     $t1    0   label5    #case: 0, Object
    bgt     $t1    5   label5    #case: 5, Object
    sw      $a0    20($fp)                #case: o

    la      $a0     str_const0           #literal, object\n

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label0      #call: protect from dispatch to void
    la      $a0    str_const2               #call: constant object with name of the file
    li      $t1    10                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label0:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    12($t1)              #call: method out_string is at offset 12
    jalr    $t1

    b       label3                       #case: go to end
label5:

    jal     _case_abort                     #case: default
label3:

    lw      $fp    24($sp)         #outm: restore 24
    lw      $s0    20($sp)         #outm: restore 20 (self)
    lw      $ra    16($sp)         #outm: restore 16
#outm: Clean everything! restore sp, 0 from formals, 3 from local frame
    addiu   $sp    $sp    24
    jr      $ra                        #outm: jump and make happy the callee
