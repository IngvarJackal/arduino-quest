#include <UTFT.h>
#include <memorysaver.h>
#include <TimerThree.h>
#include <Tone.h>
#include <SPI.h>
#include <SD.h>

const char PIN_UP = 7;
const char PIN_ENTER = 6;
const char PIN_DOWN = 5;

UTFT tft(CTE32HR,38,39,40,41);
extern uint8_t SmallFont[];

Tone tone1;
Tone tone2;

/*int melody[] =  {880,  0, 784,  0, 523,  0, 880,  0, 784,  0, 523,  0, 880,  0, 523,  0, 784,  0, 659,  0, 494,  0, 784,  0, 659,  0, 494,
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
                        };*/
                        
byte colors[] = {
    0, 0, 0,
    34, 32, 52,
    69, 40, 60,
    102, 57, 49,
    143, 86, 59,
    223, 113, 38,
    217, 160, 102,
    238, 195, 154,
    251, 242, 54,
    153, 229, 80,
    106, 190, 48,
    55, 148, 110,
    75, 105, 47,
    82, 75, 36,
    50, 60, 57,
    63, 63, 116,
    48, 96, 130,
    91, 110, 225,
    99, 155, 255,
    95, 205, 228,
    203, 219, 252,
    255, 255, 255,
    155, 173, 183,
    132, 126, 135,
    105, 106, 106,
    89, 86, 82,
    118, 66, 138,
    172, 50, 50,
    217, 87, 99,
    215, 123, 186,
    143, 151, 74,
    138, 111, 48};

void setup() {
  Timer3.initialize(2500);
  Timer3.attachInterrupt(processTick);
  
  tone1.begin(11);
  tone2.begin(12);
  
  tft.InitLCD(LANDSCAPE);
  SD.begin(53);

  pinMode(PIN_UP, INPUT_PULLUP);
  pinMode(PIN_ENTER, INPUT_PULLUP);
  pinMode(PIN_DOWN, INPUT_PULLUP);

  tft.setFont(SmallFont);

  Serial.begin(9600);
}

void processTick() {
  playSound();
}

bool CUR_IS_FULL;
char LASTIMG[13];
char CURIMG[13];
char CURSONG[13];
char PREVSONG[13];
char NEXTFILE[13];
char* VARNAMES[6];
byte MAXVAR = 0;
char CURVAR = 0;
char PREVVAR = 0;
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
  memcpy(LASTIMG, CURIMG, sizeof(CURIMG));
  memcpy(PREVSONG, CURSONG, sizeof(CURSONG));
  CURIMG[13] = '\0';
  CURSONG[13] = '\0';

  CURVAR = 0;
  PREVVAR = 0;

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
        //vartxt[13] = '\0';
        VARNAMES[v] = vartxt;
        MAXVAR = v;
      } else {
        free(vartxt);
      }
      v++;
    }
  }
  myFile.close();
}

unsigned char melody[256];
unsigned char noteDurations[256];
unsigned char melody2[256];
unsigned char noteDurations2[256];

unsigned char curnote = 0;
unsigned char curnote2 = 0;

unsigned char curlen = -1;
unsigned char curlen2 = -1;

bool songIsReady = false;

void playSound() {
  if (!songIsReady ) {
    return;
  }

  if (noteDurations[curnote] == 255 || noteDurations2[curnote2] == 255) {
    curnote = 0;
    curlen = noteDurations[curnote];
    curnote2 = 0;
    curlen2 = noteDurations2[curnote2];
  }
  
  if (curlen <= 0) {
    curnote++;
    curlen = noteDurations[curnote];
    
    if (melody[curnote] == 0) {
      tone1.stop();
    } else {
      tone1.play(TONES[melody[curnote]]);
    }    
  } else {
    curlen--;
  }

  if (curlen2 <= 0) {
    curnote2++;
    curlen2 = noteDurations2[curnote2];
    
    if (melody2[curnote2] == 0) {
      tone2.stop();
    } else {
      tone2.play(TONES[melody2[curnote2]]);
    }    
  } else {
    curlen2--;
  }
}

void loadSong() {
  if (strcmp(PREVSONG, CURSONG) == 0) {
    return;
  }
  myFile = SD.open(CURSONG);
  unsigned char c;
  for (char i=0; ; i++) {
    c = myFile.read();
    melody[i] = c;
    if (c == 0xFF)
      break;
  }
  for (char i=0; ; i++) {
    c = myFile.read();
    noteDurations[i] = c;
    if (c == 0xFF)
      break;
  }
  for (char i=0; ; i++) {
    c = myFile.read();
    melody2[i] = c;
    if (c == 0xFF)
      break;
  }
  for (char i=0; ; i++) {
    c = myFile.read();
    noteDurations2[i] = c;
    if (c == 0xFF)
      break;
  }
  myFile.close();
  songIsReady = true;
}

int freeRam() {
  extern int __heap_start, *__brkval; 
  int v; 
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval); 
}

void drawAll() {
  if (strcmp(LASTIMG,CURIMG) == 0) {
    drawText();
  } else {
    drawText();
    drawImg();
  }
}

void drawText() {
  emptyTextArea();
  tft.setColor(VGA_WHITE);
  tft.setBackColor(VGA_TRANSPARENT);
  int startShift = 0;
  char line[MAX_X];
  for (int lineNum=0;; lineNum++) {
    for (int i=0; i<MAX_X; i++) {
      line[i] = '\0';
    }
    for (int i = startShift; i < sizeof(TEXT); i++) {
      if (TEXT[i] != '\0' && TEXT[i] != '\n') {
        line[i-startShift] = TEXT[i];
      } else {
        startShift = i+1;
        break;
      }
    }
    tft.print(line, 160, 10*lineNum);
    if (TEXT[startShift-1] == '\0') {
      return;
    }
  }
}

void drawVariants() {
  emptyTextArea();
  tft.setColor(VGA_WHITE);
  tft.setBackColor(VGA_TRANSPARENT);
  for (int i=0; i < MAXVAR; i++) {
    tft.print(VARNAMES[i], 160,10*i);
  }
  selectVariant();
}

void selectVariant() {
  tft.setColor(VGA_WHITE);
  tft.setBackColor(VGA_BLACK);
  tft.print(VARNAMES[PREVVAR], 160, 10*PREVVAR);
  tft.setColor(VGA_BLACK);
  tft.setBackColor(VGA_WHITE);
  tft.print(VARNAMES[CURVAR], 160, 10*CURVAR);
}


void setPixel(byte r, byte g, byte b, int x, int y) {
  tft.setColor(r,g,b);
  tft.drawPixel(x*2,y*2); tft.drawPixel(x*2+1,y*2);
  tft.drawPixel(x*2,y*2+1); tft.drawPixel(x*2+1,y*2+1);
}

void drawImg() {
  emptyImageArea();
  myFile = SD.open(CURIMG);
  int rowLen = myFile.read()*256;
  rowLen += myFile.read();
  int row = 0;
  for (int col=0; myFile.available(); col++) {
    if (col%rowLen == 0 && col != 0) {
      row++;
    }
    char color = myFile.read();
    setPixel(colors[color*3 + 0], colors[color*3 + 1], colors[color*3 + 2], col%rowLen, row);
  }
  myFile.close();
}


void emptyImageArea() {
  tft.setColor(VGA_BLACK);
  tft.fillRect(0, 0, 160-1, tft.getDisplayYSize()-1);
}


void emptyTextArea() {
  tft.setColor(VGA_BLACK);
  tft.fillRect(160, 0, tft.getDisplayXSize()-1, tft.getDisplayYSize()-1);
}

void readInput() {
  while (true) {
    if (digitalRead(PIN_UP) == 0 && CURVAR > 0) {
      PREVVAR = CURVAR;
      CURVAR--;
      selectVariant();
      delay(250);
    } else if (digitalRead(PIN_ENTER) == 0) {
      return;
    } else if (digitalRead(PIN_DOWN) == 0 && CURVAR < MAXVAR-1) {
      PREVVAR = CURVAR;
      CURVAR++;
      selectVariant();
      delay(250);
    }
  }
}

int y = 0;
void loop() {
  tft.clrScr();
  tft.printNumI(freeRam(), 0, 200);
  delay(1000);
  
  parseFile("00000001.TXT");
  loadSong();
  drawAll();
  delay(6000);

  drawVariants();
  readInput();
}
