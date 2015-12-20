#include <UTFT.h>
#include <memorysaver.h>
#include <TimerThree.h>
#include <Tone.h>
#include <SPI.h>
#include <SD.h>

UTFT tft(CTE32HR,38,39,40,41);
extern uint8_t SmallFont[];

Tone tone1;
Tone tone2;

int melody[] =  {880,  0, 784,  0, 523,  0, 880,  0, 784,  0, 523,  0, 880,  0, 523,  0, 784,  0, 659,  0, 494,  0, 784,  0, 659,  0, 494,
                 0, 784,  0, 659,  0, 523,  0, 440,  0, 659,  0, 523,  0, 440,  0, 659,  0, 523,  0, 440,  0, 659,  0, 523,  0, 494,  0, 440,  0, 494,  0,
                 523,  0, 659,  0, 784,  0, 880,  0, 698,  0, 523,  0, 880,  0, 698,  0, 523,  0, 1047,  0, 988,  0, 784,  0, 659,  0, 494,  0, 392,  0, 330,
                 0, 392,  0, 440,  0, 494,  0, 523,  0, 440,  0, 330,  0, 523,  0, 440,  0, 330,  0, 523,  0, 330,  0, 523,  0, 440,  0, 330,  0, 523,  0,
                 587,  0, 494,  0, 392,  0, 494,  0
                };


byte noteDurations[] = { 0,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,
                         21,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  3,
                         3,  3,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3, 21,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  3,  3,  3,  3,
                         9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3,  9,  3
                       };

int melody2[] = {175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 165,  0, 165,  0, 165,  0, 165,  0, 165,  0, 165,
                 0, 165,  0, 165,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0,
                 110,  0, 110,  0, 110,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 175,  0, 165,  0, 165,  0, 165,  0, 165,  0, 165,
                 0, 165,  0, 165,  0, 165,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0, 110,  0,
                 98,  0, 98,  0, 98,  0, 98,  0
                };

byte noteDurations2[] = { 0,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
                          6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
                          6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,
                          6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6,  6
                        };


void setup(){
  Timer3.initialize(20000);
  //Timer3.attachInterrupt(processTick);
  
  tone1.begin(11);
  tone2.begin(12);
  
  tft.InitLCD(LANDSCAPE);
  SD.begin(53);

  Serial.begin(9600);
}

int curnote = -1;
int curlen = -1;
int curnote2 = -1;
int curlen2 = -1;
void playSound(int tick) {
  if (curlen <= 0) {
    curnote += 1;
    curlen = noteDurations[curnote % 127];
    if (melody[curnote % 127] == 0) {
      tone1.stop();
    } else {
      tone1.play(melody[curnote % 127]);
    }
      if (melody2[curnote % 127] == 0) {
      tone2.stop();
    } else {
      tone2.play(melody2[curnote % 127]);
    }
  } else {
    curlen--;
  }
}

int tick = 0;
void processTick() {
  tick++;
  playSound(tick);
}

bool CUR_IS_FULL;
char CURIMG[13];
char CURSONG[13];
char NEXTFILE[13];
char* VARNAMES[6];
const char* VARNAMES_DEFAULT[6] = {"", "", "", "", "", ""};
char* VARFILES[6];
char TEXT[1024];
const char FULL_START = 1;
const char TEXT_END = 3;
const char NEWLINE = '\n';
const byte MAX_X = 39;
File myFile;

void parseFile(char *filename) {
  TEXT[0] = '\0';
  NEXTFILE[0] = '\0';
  NEXTFILE[13] = '\0';
  CURIMG[13] = '\0';
  CURSONG[13] = '\0';

  for (int i=0; i<sizeof(VARNAMES)/sizeof(int); i++) {
    if (VARNAMES[i] != "") {
      free(VARNAMES[i]);
      free(VARFILES[i]);
    }
  }
  
  memcpy(VARNAMES, VARNAMES_DEFAULT, sizeof(VARNAMES_DEFAULT));
  myFile = SD.open(filename);
  for (int i=0; i<12; i++) {
    CURSONG[i] = myFile.read();
  }
  if (myFile.read() == FULL_START) {
    for (int i=0; i<12; i++) {
      CURIMG[i] = myFile.read();
    }
    for (int i=0; i<12 && myFile.available(); i++) {
      NEXTFILE[i] = myFile.read();
    }
  } else {
    for (int i=0; i<12; i++) {
      CURIMG[i] = myFile.read();
    }
    char c;
    for (int i=0; i<1024; i++) {
      c = myFile.read();
      if (c == TEXT_END) {
        break;
      } else {
        TEXT[i] = c;
      }
    }
    char vartxtDefault[MAX_X];
    for (int i=0; i<MAX_X; i++) {
      vartxtDefault[i] = '\0';
    }
    int v = 0;
    while (myFile.available()) {
      char* vartxt = (char*)malloc(MAX_X);
      memcpy(vartxt, vartxtDefault, sizeof(vartxtDefault));
      if (v != 0) {
        char* varfile = (char*)malloc(13);
        for (int i=0; i<12; i++) {
           varfile[i] = myFile.read();
        }
        varfile[12] = '\0';
        VARFILES[v-1] = varfile;
      }
      for (int i=0; myFile.available(); i++) {
        c = myFile.read();
        if (c == TEXT_END) {
          break;
        } else {
          vartxt[i] = c;
        }
      }
      if (vartxt[0] != '\0') {
        vartxt[13] = '\0';
        VARNAMES[v] = vartxt;
      } else {
        free(vartxt);
      }
      v++;
    }
  }
  myFile.close();
}

int freeRam () 
{
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}

int y = 0;
void loop() {
  tft.clrScr();
  tft.setColor(VGA_BLACK);
  tft.fillRect(0,0, tft.getDisplayXSize()-1, tft.getDisplayYSize()-1);

  tft.setFont(SmallFont);
  
  tft.setColor(VGA_WHITE);
  tft.setBackColor(VGA_TRANSPARENT);

  parseFile("00000002.TXT");

  

  /*for (int i=0; i<sizeof(VARFILES)/sizeof(int); i++) {
    tft.print(VARFILES[i], 0, 10*i);
    if (SD.exists(VARFILES[i])) {
      tft.print("EXISTS", 14*8, 10*i);
    } else {
      tft.print("NOT EXISTS", 14*8, 10*i);
    }
    Serial.println(VARFILES[i]);
  }
  tft.printNumI(freeRam(), 0, 200);*/
  
  Serial.print("CUR_IS_FULL: ");
  Serial.println(CUR_IS_FULL);
  Serial.print("CURIMG: ");
  Serial.println(CURIMG);
  Serial.print("CURSONG: ");
  Serial.println(CURSONG);
  Serial.print("NEXTFILE: ");
  Serial.println(NEXTFILE);
  Serial.print("VARNAMES[0]: ");
  Serial.println(VARNAMES[0]);
  Serial.print("VARFILES[0]: ");
  Serial.println(VARFILES[0]);
  Serial.print("TEXT: ");
  Serial.println(TEXT);
  Serial.println();

  delay(5000);


  /*File myFile;
  char privet2[200];
  int c;
  myFile = SD.open("1.TXT");
  for (int i=0; myFile.available(); i++) {
      privet2[i] = myFile.read();
      if (i > 0 && i%2==0)
        c = privet2[i];
        c = c * 256;
        c = c + privet2[i] - 1;
        Serial.println(c);
  }

  myFile.close();

  printRus(tft, privet2, 0, 195,0);
  printRus(tft, privet2, 0, 205,0);
  
  Serial.println(strlen(privet2));*/
}
