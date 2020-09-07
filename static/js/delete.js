function checkAll() 
{ 
var code_Values = document.getElementsByTagName("input"); 
for(i = 0;i < code_Values.length;i++){ 
if(code_Values[i].type == "checkbox") 
{ 
code_Values[i].checked = true; 
} 
} 
} 
function uncheckAll() 
{ 
var code_Values = document.getElementsByTagName("input"); 
for(i = 0;i < code_Values.length;i++){ 
if(code_Values[i].type == "checkbox") 
{ 
code_Values[i].checked = false; 
} 
} 
} 
function multipleDelete() 
{ 
if (document.BuCodeSearch.elements["code_Value"]) 
{ 
var num = 0; 
var fm = document.BuCodeSearch; 
if (document.BuCodeSearch.elements["code_Value"]) 
{ 
var elm = document.BuCodeSearch.elements["code_Value"]; 
var ename = "code_Value"; 
if (elm.length) { 
var len = fm.elements[ename].length; 
for (var i = 0; i< len; i++) { 
var e = fm.elements[ename][i]; 
if (e.checked == true){ 
num++; 
} 
} 
} else { 
if (elm.checked == true ) { 
num++; 
} 
} 
if (num > 0 ) 
{ 
document.BuCodeSearch.action = '<%=EusUtil.getPage("lookup.generic.bucode.delete.s")%>'; 
document.BuCodeSearch.submit(); 
} 
} 
} 
} 
