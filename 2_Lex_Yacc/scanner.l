%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int position = 0; 
int st_position = 0; 
char symbol_table[100][20]; 
int st_indices[100]; 

void add_to_symbol_table(const char* symbol) {
    for (int i = 0; i < st_position; i++) {
        if (strcmp(symbol_table[i], symbol) == 0) {
            return; 
        }
    }
    strcpy(symbol_table[st_position], symbol);
    st_indices[st_position] = st_position + 1; 
    st_position++;
}

int get_symbol_index(const char* symbol) {
    for (int i = 0; i < st_position; i++) {
        if (strcmp(symbol_table[i], symbol) == 0) {
            return st_indices[i]; 
        }
    }
    return 0; 
}

void print_pif(const char* type, const char* value) {
    int index = get_symbol_index(value);
    printf("%s %d\n", type, index);
    position++;
}

%}

%option noyywrap

%%

int               { print_pif("Keyword: int", "int"); }
char              { print_pif("Keyword: char", "char"); }
struct            { print_pif("Keyword: struct", "struct"); }
if                { print_pif("Keyword: if", "if"); }
else              { print_pif("Keyword: else", "else"); }
while             { print_pif("Keyword: while", "while"); }
do                { print_pif("Keyword: do", "do"); }
read              { print_pif("Keyword: read", "read"); }
write             { print_pif("Keyword: write", "write"); }
"("               { print_pif("Separator: (", "("); }
")"               { print_pif("Separator: )", ")"); }
"{"               { print_pif("Separator: {", "{"); }
"}"               { print_pif("Separator: }", "}"); }
","               { print_pif("Separator: ,", ","); }
";"               { print_pif("Separator: ;", ";"); }
"."               { print_pif("Separator: .", "."); }
[ \t\n]          ; 
"+"               { print_pif("Addition/Subtraction Operator: +", "+"); }
"-"               { print_pif("Addition/Subtraction Operator: -", "-"); }
"*"               { print_pif("Multiplication/Division Operator: *", "*"); }
"/"               { print_pif("Multiplication/Division Operator: /", "/"); }
"%"               { print_pif("Multiplication/Division Operator: %", "%"); }
":="              { print_pif("Assignment Operator: :=", ":="); }
"<"               { print_pif("Relational Operator: <", "<"); }
"<="              { print_pif("Relational Operator: <=", "<="); }
"="               { print_pif("Relational Operator: =", "="); }
">="              { print_pif("Relational Operator: >=", ">="); }
"!="              { print_pif("Relational Operator: !=", "!="); }
[a-z][a-z0-9_]*  { add_to_symbol_table(yytext); print_pif("Identifier", yytext); }
[+-]?[0-9]+      { add_to_symbol_table(yytext); print_pif("Integer Constant", yytext); }
'\''[a-z0-9]'\''  { add_to_symbol_table(yytext); print_pif("Character Constant", yytext); }
\"([^\"\\]|\\.)*\"  { add_to_symbol_table(yytext); print_pif("String Constant", yytext); }
.                { print_pif("Unrecognized character", yytext); }

%%

int main(int argc, char **argv) {
    FILE *file;

    if (argc > 1) {
        file = fopen(argv[1], "r");
        if (file == NULL) {
            perror("Error opening file");
            return EXIT_FAILURE;
        }
        yyin = file;
    }

    printf("PIF:\n");
    yylex();
    
    printf("\n\nSymbol Table:\n");
    for (int i = 0; i < st_position; i++) {
        printf("%s %d\n", symbol_table[i], st_indices[i]);
    }

    if (file) fclose(file);
    return 0;
}
