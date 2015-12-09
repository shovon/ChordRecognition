%Parameters for Chord Recognition

%-----Basis Functions
global BASISTYPE VERT HORZ BO;
BASISTYPE = 1;  %0 = BREVE, 1 = JEFF's
VERT = 70;
HORZ = 33;
BO = [VERT+1, VERT+HORZ];

%-----Chord labels
global ALLCHORDS_L CHORD_MAP CHORD_L CHORD_M CHORD_A K;
%type = {'M' 'M4' 'M6' 'V' 'm' 'm7' 'd' 'd7'};

ALLCHORDS_L = {'M' 'M4' 'M6' 'M7' 'V' 'm' 'm6' 'm7' 'd' 'd7' 'hd7'};
ALLCHORDS_M = [ 0   0    0    0    3   1   1    1    2   2    2]; %Mode: 0 = M, 1 = m, 2 = d, 3 = V
ALLCHORDS_A = [ 0   5    9    11   10  0   9    10   0   9    10]; %Added Note: in semitones

%All Chords (132 labels)
%CHORD_MAP   = ALLCHORDS_L;
%CHORD_L     = ALLCHORDS_L;

%BREVE Chords (108 labels)
%CHORD_MAP   = {'M' 'M4' 'M6' 'V' 'V' 'm' 'm6' 'm7' 'd' 'd7' 'd7'};
%CHORD_L     = {'M' 'M4' 'M6' 'V' 'm' 'm6' 'm7' 'd' 'd7'};

%KP Chords (108 labels)
%CHORD_MAP   = {'M' 'M'  'M' 'M7' 'V' 'm' 'm6' 'm7' 'd' 'd7' 'hd7'};
%CHORD_L     = {'M' 'M7' 'V' 'm' 'm6' 'm7' 'd' 'd7' 'hd7'};

%Simple Model (36 labels)
CHORD_MAP   = {'M' 'M'  'M'  'M'  'M' 'm' 'm'  'm'  'd' 'd'  'd'};
CHORD_L     = {'M' 'm' 'd'};


CHORD_M = ALLCHORDS_M(ismember(ALLCHORDS_L, CHORD_L));
CHORD_A = ALLCHORDS_A(ismember(ALLCHORDS_L, CHORD_L));
K = size(CHORD_L,2)*12; % number of labels

%-----Dataset
%[X,T] = parseDataset('Datasets/allchords.f1');
[X,T] = parseDataset('Datasets/jsbach2.f1');
%[X,T] = parseDataset('Datasets/kp1.f1');
N = size(X,2); % number of training examples


