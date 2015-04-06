var school={
	"AAAA":0,
	"BBBB":1,
	"CCCC":2,
	"DDDD":3,
	"EEEE":4,
};
var dept={
	"AAA":0,
	"BBB":0,
	"AAD":0,
	"AAE":0,
	"AAC":1,
	"CCC":2,
	"DD":3,
	"EE":4,
};
var deptNames=[
	"AAA",
	"BBB",
	"AAD",
	"AAE",
	"AAC",
	"CCC",
	"DD",
	"EE",
];
var deptIndex={
	"AAA":0,
	"BBB":1,
	"AAD":2,
	"AAE":3,
	"AAC":4,
	"CCC":5,
	"DD":6,
	"EE":7,
};
var deptIndexS={
	"AAA":0,
	"BBB":1,
	"AAD":2,
	"AAE":3,
	"AAC":0,
	"CCC":0,
	"DD":0,
	"EE":0,
};
var schoolList=["AAAA","BBBB","CCCC","DDDD","EEEE"];
var schoolOffset = [0,4,5,6,7,8];
function getSchoolName(departmentName){    return schoolList[dept[departmentName]];}
function getSchoolIndex(departmentName) {    return dept[departmentName];}