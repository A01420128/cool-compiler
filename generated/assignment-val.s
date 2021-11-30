
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
    .word   8
    .word   String_dispTab
    .word   int_const5
    .ascii  "--filename--"
    .byte   0
    .align  2

    .word   -1
str_const2:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const2
    .ascii  "\n"
    .byte   0
    .align  2

    .word   -1
str_const1:
    .word   4
    .word   6
    .word   String_dispTab
    .word   int_const6
    .ascii  "\ny: "
    .byte   0
    .align  2

    .word   -1
str_const0:
    .word   4
    .word   5
    .word   String_dispTab
    .word   int_const3
    .ascii  "x: "
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
    .word   5

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
    .word    Main.f
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
    .word    0
    .word    -1
Bool_protObj:
    .word    3
    .word    4
    .word    Bool_dispTab
    .word    0
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

Main.f:
    addiu   $sp    $sp    -12        #inm: frame has 0 locals
    sw      $fp    12($sp)         #inm: save $fp
    sw      $s0    8($sp)         #inm: save $s0 (self)
    sw      $ra    4($sp)         #inm: save $ra
    addiu   $fp    $sp    4           #inm: $fp points to locals
    move    $s0    $a0                #inm: self to $s0

    la      $a0     str_const0           #literal, x: 

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label0      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    3                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label0:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    12($t1)              #call: method out_string is at offset 12
    jalr    $t1

    lw      $a0     12($fp)            #obj: load [x], Int

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label1      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    4                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label1:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    16($t1)              #call: method out_int is at offset 16
    jalr    $t1

    la      $a0     str_const1           #literal, \ny: 

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label2      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    5                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label2:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    12($t1)              #call: method out_string is at offset 12
    jalr    $t1

    lw      $a0     16($fp)            #obj: load [y], Int

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label3      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    6                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label3:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    16($t1)              #call: method out_int is at offset 16
    jalr    $t1

    la      $a0     str_const2           #literal, \n

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label4      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    7                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label4:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    12($t1)              #call: method out_string is at offset 12
    jalr    $t1

    lw      $fp    12($sp)         #outm: restore 12
    lw      $s0    8($sp)         #outm: restore 8 (self)
    lw      $ra    4($sp)         #outm: restore 4
#outm: Clean everything! restore sp, 8 from formals, 0 from local frame
    addiu   $sp    $sp    20
    jr      $ra                        #outm: jump and make happy the callee

Main.main:
    addiu   $sp    $sp    -16        #inm: frame has 1 locals
    sw      $fp    16($sp)         #inm: save $fp
    sw      $s0    12($sp)         #inm: save $s0 (self)
    sw      $ra    8($sp)         #inm: save $ra
    addiu   $fp    $sp    4           #inm: $fp points to locals
    move    $s0    $a0                #inm: self to $s0

    
    la      $a0     int_const2           #literal, 2

    sw      $a0     0($fp)            #letdecl: initial value of x

    
    la      $a0     int_const3           #literal, 3

    sw      $a0     0($fp)               #assignment of x

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    
    la      $a0     int_const4           #literal, 4

    sw      $a0     0($fp)               #assignment of x

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label5      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    11                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label5:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    28($t1)              #call: method f is at offset 28
    jalr    $t1

    lw      $a0     0($fp)            #obj: load [x], Int

    sw      $a0    0($sp)                 #call: push Param
    addiu   $sp    $sp        -4          #call:

    move    $a0    $s0                    #call: get self into $a0

    bne     $a0    $zero      label6      #call: protect from dispatch to void
    la      $a0    str_const3               #call: constant object with name of the file
    li      $t1    12                   #call: line number
    jal    _dispatch_abort                  #call: message and die
label6:

    lw      $t1    8($a0)                 #call: ptr to dispatch table
    lw      $t1    16($t1)              #call: method out_int is at offset 16
    jalr    $t1

    lw      $fp    16($sp)         #outm: restore 16
    lw      $s0    12($sp)         #outm: restore 12 (self)
    lw      $ra    8($sp)         #outm: restore 8
#outm: Clean everything! restore sp, 0 from formals, 1 from local frame
    addiu   $sp    $sp    16
    jr      $ra                        #outm: jump and make happy the callee
