// 注释测试
#define comment_test/**/123                                   //注释应该替换为空白字符，而不是直接删掉，值为123而不是none
#define     comment_test0 -123 //多空格
#define 		comment_test1 -100                            //多tab
///**/// #define comment_test0                                //行开头两种注释
/**///// #define comment_test1
#define comment_test2 " 0x20 // /**/ "                        //带注释的字符串
#define comment_test3 //"0x20///*"                            //单行注释，含/**/注释和双引号
#define comment_test4 /* //"//"                               //多行注释1，内含单行注释和双引号，多行注释后没有字符

*/
#define comment_test5 /*多行注释2 //"//"                      //同上，只不过中间多了空行
非空行
*/
/*注释*/ #define /*注释*/ comment_test6 /*注释*/ -123 /*注释*/           //行内多个/**/注释
#define/*                                                    //跨行注释，注释后有非注释字符。

*/ comment_test7
/*

*/ 


// 指令间空格测试
# define def1                                                   
#  define def2 //空格
#	define def3 //tab
    # define def4
    #	define def5 /*
    */ 123123


// 整形后缀判断
#define int1 123u
#define int2 123U
#define int3 123l
#define int4 123ll
#define int5 123ul
#define int6 123ull
#define int7 123ui64 


// 浮点数测试
#define float1 15.75
#define float2 1.575E1
#define float1 1575e-2
#define float1 -2.5e-3
#define float1 25E-4


// 字符串测试 
#define str1 "\n \r \t \\"                                      //简单的字符串转义
#define str2 L"str1," L"str2," L"str3"                          //宽字符串拼接，不用考虑 ##拼接，带L都转unicode
#define str3 "str1," L"str2," L"str3"
#define str4 L"" "str1,""str2"
#define str5 "str1," "str2," "str3"                             //普通字符串拼接
#define str6 "\v\'\"\f \"\n\r\t\b\a\\"                    //字符串转义，注意dumpdict的结果


// 字符测试 
#define char1 '\t' 
#define char2 'a'                        
#define char3 '\010'
#define char4 '\x008'
#define char5 '\\'                        


// 整形进制转换
#define int8 010
#define int9 0x10
    
    
// 聚合测试
#define agg1 	{1,{2,3,","},','}
#define agg2    {"{", "}" ,"," ,'{', '}' , ','}                 //字符中的{、}、，
#define agg3    {"'", '"'}                                      //引号测试
#define agg4    {",", ','}                                      //逗号测试
#define agg5    {"abc,def","", " ","	",{{1,   2,3}}, {   },{}, { 1},{1 },{1},{"",    }   }
#define agg6    {"123{1e1231.2}"}
#define agg7    {"abc,def", {"", ' '}}                          //聚合
#define agg8    {"\v\'\"\f \"\n\r\t\b\a\\"}              //聚合内字符串转义
#define agg9 {};
    

