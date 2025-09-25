#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>




enum nome_token{
    FUNCTION,
    MAIN,
    LET,
    INT,
    FLOAT,
    CHAR,
    IF,
    ELSE,
    WHILE,
    PRINTLN,
    RETURN,
    LBRACKET,
    RBRACKET,
    LBRACE,
    RBRACE,
    ARROW,
    COLON,
    SEMICOLON,
    COMMA,
    ASSIGN,
    EQ,
    NE,
    GT,
    GE,
    LT,
    LE,
    PLUS,
    MINUS,
    MULT,
    DIV,
    ID,
    INT_CONST,
    FLOAT_CONST,
    CHAR_LITERAL,
    FMT_STRING
};

typedef struct {
    char lexema[99];
    int num_linha;
    enum nome_token sla;
}token;

token criar_token(char lexema_temp, int num_linha, enum nome_token seisim){
    token temp;

    strcpy(temp.lexema, lexema_temp);
    temp.num_linha = num_linha;
    temp.sla = seisim;

    return temp;
}




void main(){
    
    token vetor_de_tonkes[100];
    int controlador_tonkens = 0;
    int estado = 0;
    char lexema_temp[100];
    char vetor[1000];
    int num_linha = 0;
    int i = 0;
    bool USOU_ULTIMO = false;
    while (i < 1000){
        USOU_ULTIMO = true;
        char c = vetor[i];
        switch(estado){
            case 0: 
                if(c == '('){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, LBRACKET);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == ')'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, RBRACKET);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == '{'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, LBRACE);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == '}'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, RBRACE);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == ':'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, COLON);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == ';'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, SEMICOLON);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == ','){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, COMMA);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == '+'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, PLUS);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == '*'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, MULT);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == '/'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, DIV);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else if (c == '\n'){
                    num_linha++;
                    estado = 0;
                } else if (c == ' '){
                    estado = 0;
                } else if (c == '-'){
                    strcat(lexema_temp, c);
                    estado = 1;
                } else if (c == '!'){
                    strcat(lexema_temp, c);
                    estado = 2;
                } else if (c == '='){
                    strcat(lexema_temp, c);
                    estado = 3;
                } else if (c == '>'){
                    strcat(lexema_temp, c);
                    estado = 4;
                }
                
                break;

            case 1:
                if(c == '>'){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, ARROW);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else {
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, MINUS);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                    USOU_ULTIMO = false;
                }   
                break;
            case 2:
                if(c == '='){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, NE);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else {
                    printf("ERRO NA LINHA: %d\n", num_linha);
                    estado = 0;
                }
                break;
            case 3:
                if(c == '='){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, EQ);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else {
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, ASSIGN);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                    USOU_ULTIMO = false;
                }
                break;
            case 4:
                if(c == '='){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, GE);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else {
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, GT);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                    USOU_ULTIMO = false;
                }
                break;
            
            case 5:
                if(c == '='){
                    strcat(lexema_temp, c);
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, LE);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                } else {
                    vetor_de_tonkes[controlador_tonkens] = criar_token(lexema_temp, num_linha, LT);
                    controlador_tonkens++;
                    estado = 0;
                    strcpy(lexema_temp, "");
                    USOU_ULTIMO = false;
                }
                break;
            case 6:
                
            default:
                return 87;
            
        }
        if(c == '\n'){
            num_linha++;
        }

        if(USOU_ULTIMO == true){
            i++;
        }
    }


}