	.data	 
	.align	2 
	.globl	class_nameTab 
	.globl	Main_protObj 
	.globl	Int_protObj 
	.globl	String_protObj 
	.globl	bool_const0 
	.globl	bool_const1 
	.globl	_int_tag 
	.globl	_bool_tag 
	.globl	_string_tag 
_int_tag:
	.word	2 
_bool_tag:
	.word	3 
_string_tag:
	.word	4 
	.globl	_MemMgr_INITIALIZER 
_MemMgr_INITIALIZER:
	.word	_NoGC_Init 
	.globl	_MemMgr_COLLECTOR 
_MemMgr_COLLECTOR:
	.word	_NoGC_Collect 
	.globl	_MemMgr_TEST 
_MemMgr_TEST:
	.word	0 
	.word	-1
str_const11:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const0
	.byte	0	
	.align	2
	.word	-1
str_const10:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const1
	.ascii	"Main"
	.byte	0	
	.align	2
	.word	-1
str_const9:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const2
	.ascii	"String"
	.byte	0	
	.align	2
	.word	-1
str_const8:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const1
	.ascii	"Bool"
	.byte	0	
	.align	2
	.word	-1
str_const7:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const3
	.ascii	"Int"
	.byte	0	
	.align	2
	.word	-1
str_const6:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const4
	.ascii	"IO"
	.byte	0	
	.align	2
	.word	-1
str_const5:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const2
	.ascii	"Object"
	.byte	0	
	.align	2
	.word	-1
str_const4:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const5
	.ascii	"main\n"
	.byte	0	
	.align	2
	.word	-1
str_const3:
	.word	4
	.word	6
	.word	String_dispTab
	.word	int_const6
	.ascii	"object\n"
	.byte	0	
	.align	2
	.word	-1
str_const2:
	.word	4
	.word	8
	.word	String_dispTab
	.word	int_const7
	.ascii	"<basic class>"
	.byte	0	
	.align	2
	.word	-1
str_const1:
	.word	4
	.word	5
	.word	String_dispTab
	.word	int_const8
	.ascii	"\n"
	.byte	0	
	.align	2
	.word	-1
str_const0:
	.word	4
	.word	8
	.word	String_dispTab
	.word	int_const9
	.ascii	"--filename--"
	.byte	0	
	.align	2
	.word	-1
int_const9:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	12
	.word	-1
int_const8:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	1
	.word	-1
int_const7:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	13
	.word	-1
int_const6:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	7
	.word	-1
int_const5:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	5
	.word	-1
int_const4:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	2
	.word	-1
int_const3:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	3
	.word	-1
int_const2:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	6
	.word	-1
int_const1:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	4
	.word	-1
int_const0:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	0
	.word	-1
bool_const0:
	.word	3
	.word	4
	.word	Bool_dispTab
	.word	0
	.word	-1
bool_const1:
	.word	3
	.word	4
	.word	Bool_dispTab
	.word	1
class_nameTab:
	.word	str_const5
	.word	str_const6
	.word	str_const7
	.word	str_const8
	.word	str_const9
	.word	str_const10
class_objTab:
	.word	Object_protObj 
	.word	Object_init 
	.word	IO_protObj 
	.word	IO_init 
	.word	Int_protObj 
	.word	Int_init 
	.word	Bool_protObj 
	.word	Bool_init 
	.word	String_protObj 
	.word	String_init 
	.word	Main_protObj 
	.word	Main_init 
Object_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
IO_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
Int_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
Bool_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
String_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	String.length
	.word	String.concat
	.word	String.substr
Main_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
	.word	Main.main
	.word	-1 
Object_protObj:
	.word	0 
	.word	3 
	.word	Object_dispTab 
	.word	-1 
IO_protObj:
	.word	1 
	.word	3 
	.word	IO_dispTab 
	.word	-1 
Int_protObj:
	.word	2 
	.word	4 
	.word	Int_dispTab 
	.word	0 
	.word	-1 
Bool_protObj:
	.word	3 
	.word	4 
	.word	Bool_dispTab 
	.word	0 
	.word	-1 
String_protObj:
	.word	4 
	.word	5 
	.word	String_dispTab 
	.word	int_const0 
	.word	0 
	.word	-1 
Main_protObj:
	.word	5 
	.word	3 
	.word	Main_dispTab 
	.globl	heap_start 
heap_start:
	.word	0 
	.text	 
	.globl	Main_init 
	.globl	Int_init 
	.globl	String_init 
	.globl	Bool_init 
	.globl	Main.main 
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
	jal	Object_init 
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
	jal	Object_init 
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
	jal	Object_init 
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
	jal	Object_init 
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
	jal	IO_init 
	move	$a0 $s0 
	lw	$fp 12($sp) 
	lw	$s0 8($sp) 
	lw	$ra 4($sp) 
	addiu	$sp $sp 12 
	jr	$ra 
Main.main:
	addiu	$sp $sp -24 		# m: frame has 3 locals
	sw	$fp 24($sp) 		# m: save $fp
	sw	$s0 20($sp) 		# m: save $s0 (self)
	sw	$ra 16($sp) 		# m: save $ra
	addiu	$fp $sp 4 		# m: $fp points to locals
	move	$s0 $a0 		# m: self to $s0
	move	$a0 $s0 
	sw	$a0 8($fp) 		# letd: Store initial value of thing
	lw	$a0 8($fp) 		# load [thing], class cool.structure.Local
	bne	$a0 $zero label1 	# case: protect from case on void
	la	$a0 str_const0 
	li	$t1 -1 			# case: line number
	jal	_case_abort2 
label1:
	lw	$t1 0($a0) 		# case: load obj tag
	blt	$t1 5 label2 		# case: Main min
	bgt	$t1 5 label2 		# case: Main max
	sw	$a0 4($fp) 		# case: save value on local [m]
	la	$a0 str_const4 
	sw	$a0 0($sp) 		# call: Push parameter
	addiu	$sp $sp -4 
	move	$a0 $s0 
	bne	$a0 $zero label3 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 11 			# call: line number
	jal	_dispatch_abort 
label3:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 12($t1) 		# call: method out_string is offset 3
	jalr	$t1 
	b	label0 			# case: go to end
label2:
	blt	$t1 0 label4 		# case: Object min
	bgt	$t1 5 label4 		# case: Object max
	sw	$a0 0($fp) 		# case: save value on local [o]
	la	$a0 str_const3 
	sw	$a0 0($sp) 		# call: Push parameter
	addiu	$sp $sp -4 
	move	$a0 $s0 
	bne	$a0 $zero label5 	# call: protect from dispatch to void
	la	$a0 str_const0 
	li	$t1 10 			# call: line number
	jal	_dispatch_abort 
label5:
	lw	$t1 8($a0) 		# call: ptr to dispatch table
	lw	$t1 12($t1) 		# call: method out_string is offset 3
	jalr	$t1 
	b	label0 			# case: go to end
label4:
	jal	_case_abort 		# case: default
label0:
	lw	$fp 24($sp) 		# m: restore $fp
	lw	$s0 20($sp) 		# m: restore $s0 (self)
	lw	$ra 16($sp) 		# m: restore $ra
	addiu	$sp $sp 24 		# m: restore sp, 0 from formals, 24 from local frame
	jr	$ra 
