// ע�Ͳ���
#define comment_test/**/123                                   //ע��Ӧ���滻Ϊ�հ��ַ���������ֱ��ɾ����ֵΪ123������none
#define     comment_test0 -123 //��ո�
#define 		comment_test1 -100                            //��tab
///**/// #define comment_test0                                //�п�ͷ����ע��
/**///// #define comment_test1
#define comment_test2 " 0x20 // /**/ "                        //��ע�͵��ַ���
#define comment_test3 //"0x20///*"                            //����ע�ͣ���/**/ע�ͺ�˫����
#define comment_test4 /* //"//"                               //����ע��1���ں�����ע�ͺ�˫���ţ�����ע�ͺ�û���ַ�

*/
#define comment_test5 /*����ע��2 //"//"                      //ͬ�ϣ�ֻ�����м���˿���
�ǿ���
*/
/*ע��*/ #define /*ע��*/ comment_test6 /*ע��*/ -123 /*ע��*/           //���ڶ��/**/ע��
#define/*                                                    //����ע�ͣ�ע�ͺ��з�ע���ַ���

*/ comment_test7
/*

*/ 


// ָ���ո����
# define def1                                                   
#  define def2 //�ո�
#	define def3 //tab
    # define def4
    #	define def5 /*
    */ 123123


// ���κ�׺�ж�
#define int1 123u
#define int2 123U
#define int3 123l
#define int4 123ll
#define int5 123ul
#define int6 123ull
#define int7 123ui64 


// ����������
#define float1 15.75
#define float2 1.575E1
#define float1 1575e-2
#define float1 -2.5e-3
#define float1 25E-4


// �ַ������� 
#define str1 "\n \r \t \\"                                      //�򵥵��ַ���ת��
#define str2 L"str1," L"str2," L"str3"                          //���ַ���ƴ�ӣ����ÿ��� ##ƴ�ӣ���L��תunicode
#define str3 "str1," L"str2," L"str3"
#define str4 L"" "str1,""str2"
#define str5 "str1," "str2," "str3"                             //��ͨ�ַ���ƴ��
#define str6 "\v\'\"\f \"\n\r\t\b\a\\"                    //�ַ���ת�壬ע��dumpdict�Ľ��


// �ַ����� 
#define char1 '\t' 
#define char2 'a'                        
#define char3 '\010'
#define char4 '\x008'
#define char5 '\\'                        


// ���ν���ת��
#define int8 010
#define int9 0x10
    
    
// �ۺϲ���
#define agg1 	{1,{2,3,","},','}
#define agg2    {"{", "}" ,"," ,'{', '}' , ','}                 //�ַ��е�{��}����
#define agg3    {"'", '"'}                                      //���Ų���
#define agg4    {",", ','}                                      //���Ų���
#define agg5    {"abc,def","", " ","	",{{1,   2,3}}, {   },{}, { 1},{1 },{1},{"",    }   }
#define agg6    {"123{1e1231.2}"}
#define agg7    {"abc,def", {"", ' '}}                          //�ۺ�
#define agg8    {"\v\'\"\f \"\n\r\t\b\a\\"}              //�ۺ����ַ���ת��
#define agg9 {};
    

