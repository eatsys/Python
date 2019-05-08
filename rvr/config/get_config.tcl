proc getConfig { configFile Section Key {Comment "#"} {Equal "="}} {
      set Value ""                  ;#记录过程返回的值 
      set FindSection 0             ;#记录是否找到了section
	  # 打开配置文件
	  set err [catch {set fileid [open $configFile r]} errMsg]
      if {$err == 1} {
		puts "errMsg : $errMsg"
		return $Value
      }
	  #成功打开文件后,一行一行的加以分析
      set rowid 0                      ;#记录当前行数,程序调试时打印调试信息使用的
      seek $fileid 0 start                       ;#定位到文件头
      while {[eof $fileid] != 1} {                ;#读取文件内容
	   incr rowid                         ;#记录行数,从一开始 
       gets $fileid line	  ;#读出一行   
	   set commentpos [string first $Comment $line]       ;#得到注释符号的位置
	   if { $commentpos == 0 } {
			#行以注释符号开头，忽略掉该行
     } else {
      if { $commentpos != -1 } {       ;#行中有注释符号,去掉注释
	   set line [string range $line 0 [expr $commentpos-1]]
	  }                  
      set line [string trim $line]         ;#去掉两端的空格
	  # puts "$rowid : line : $line"
	  #如果是空就继续循环
      if { $line == "" } {                         
       continue
       } else {
		#先找section
       set linelen [string length $line]        ;#字符串长度
       set lastpos [expr $linelen - 1 ]         ;#字符串最后的位置                         
	   if { [string index $line 0] == "\[" && [string index $line $lastpos] == "\]" } {
        ;#如果是查找的section,修改标志位；如果不是相应的section,需要将标志重新赋值
          if { [string range $line 1 [expr $lastpos - 1 ]] == $Section } {  
        ;# puts "$rowid: find section : $Section"
             set FindSection 1			 
          } else {
             set FindSection 0			 
          }
       } else {
        ;#已经找到了section才继续找key		
          if { $FindSection == 1 } {
           set equalpos [string first $Equal $line]  ;#得到等号的位置
           if { $equalpos != -1} {
           #如果就是找寻的key,结束循环
			set lines [string trim [string range $line 0 [expr $equalpos - 1]]]			
            if { $lines == $Key } {
              #puts "$rowid: find key"
              set Value [string range $line [expr $equalpos + 1] [string length $line]]
              #puts "$rowid: find value: $Value"
              break
               }			
			} else {
            ;#回循环			
                 }
          } else {
        ;#回循环			
                 }
        }
       }
      }
    }
	 close $fileid
     return $Value
}

