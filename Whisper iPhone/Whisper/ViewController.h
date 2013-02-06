//
//  ViewController.h
//  testical
//
//  Created by Aran Khanna on 1/31/13.
//  Copyright (c) 2013 Aran Khanna. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreAudio/CoreAudioTypes.h>


#define REC_TIME 8

@interface ViewController : UIViewController <AVAudioRecorderDelegate>{
    
    IBOutlet UIButton *recButton;
    IBOutlet UILabel *recStateLabel;
    IBOutlet UIActivityIndicatorView *prog;
    
    BOOL isNotRecording;
    
    NSURL *temporaryRecFile;
    AVAudioRecorder *recorder;
    
}

@property(nonatomic, retain)IBOutlet UIButton *recButton;


-(IBAction)recording;
-(void)complete;


@end