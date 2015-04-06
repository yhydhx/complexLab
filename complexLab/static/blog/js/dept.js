var school={
	"CCCC":2,
	"BBBB":1,
	"DDDD":3,
	"AAAA":0,
};
var dept={
	"CCC":1,
	"DD":3,
	"AAA":0,
	"BBB":0,
};
var deptNames=[
	"CCC",
	"DD",
	"AAA",
	"BBB",
];
var deptIndex={
	"CCC":0,
	"DD":1,
	"AAA":2,
	"BBB":3,
};
var deptIndexS={
	"CCC":0,
	"DD":0,
	"AAA":0,
	"BBB":1,
};
var schoolList=["CCCC","BBBB","DDDD","AAAA"];
var schoolOffset = ["0","2","3","3"];
function getSchoolName(departmentName){    return schoolList[dept[departmentName]];}
function getSchoolIndex(departmentName) {    return dept[departmentName];}