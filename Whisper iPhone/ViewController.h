//
//  ViewController.h
//  testical
//
//  Created by Andrew Mauboussin on 1/31/13.
//  Copyright (c) 2013 Andrew Mauboussin. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreAudio/CoreAudioTypes.h>


#define REC_TIME 7

@interface ViewController : UIViewController <AVAudioRecorderDelegate>{
    
    IBOutlet UIButton *recButton;
    IBOutlet UILabel *recStateLabel;
    IBOutlet UIProgressView *prog;
    
    BOOL isNotRecording;
    
    NSURL *temporaryRecFile;
    AVAudioRecorder *recorder;
    
}

@property(nonatomic, retain)IBOutlet UIButton *recButton;


-(IBAction)recording;
-(void)complete;


@end