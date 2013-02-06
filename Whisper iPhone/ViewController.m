//
//  ViewController.m
//  testical
//
//  Created by Aran Khanna on 1/31/13.
//  Copyright (c) 2013 Aran Khanna. All rights reserved.
//

#import "ViewController.h"
#import <AVFoundation/AVFoundation.h>

@interface ViewController ()

@end

@implementation ViewController
@synthesize recButton;



-(void)complete{
    isNotRecording= YES;
    [recButton setTitle:@"Scan" forState:UIControlStateNormal];
    [prog setProgress:0.0];
    [prog setHidden:YES];
    recStateLabel.text=@"Sending";
    [recorder stop];
    
    
    dispatch_async( dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        
        NSString *theUrl = @"http://128.31.34.120:8000/upload";
        
        NSString *filePath= [temporaryRecFile path];
        
        
        
        NSData *data = [NSData dataWithContentsOfFile:filePath];
        NSMutableString *urlString = [[NSMutableString alloc] initWithFormat:@"name=myfile&&filename=myfile"];
        [urlString appendFormat:@"%@", data];
        NSData *postData = [urlString dataUsingEncoding:NSASCIIStringEncoding
                                   allowLossyConversion:NO];
        NSString *postLength = [NSString stringWithFormat:@"%d", [postData length]];
        
        NSURL *url = [NSURL URLWithString:theUrl];
        NSMutableURLRequest *urlRequest = [NSMutableURLRequest requestWithURL:url];
        [urlRequest setHTTPMethod: @"POST"];
        [urlRequest setValue:postLength forHTTPHeaderField:@"Content-Length"];
        [urlRequest setValue:@"application/x-www-form-urlencoded"
          forHTTPHeaderField:@"Content-Type"];
        [urlRequest setHTTPBody:data];
        
        
        NSData *returnData = [NSURLConnection sendSynchronousRequest:urlRequest returningResponse:nil error:nil];
        NSString *returnString = [[NSString alloc] initWithData:returnData encoding:NSUTF8StringEncoding];
        
        
        dispatch_async( dispatch_get_main_queue(), ^{
            // Add code here to update the UI/send notifications based on the
            // results of the background processing
           NSLog(@"Return String= %@",returnString);
            [recButton setHidden:NO];
           [recStateLabel setText:returnString];
        });
    });

}


-(IBAction)recording{

        isNotRecording=NO;
        [recButton setHidden:YES];
        recStateLabel.text=@"Scanning";
        temporaryRecFile = [NSURL fileURLWithPath:[NSTemporaryDirectory() stringByAppendingPathComponent:@"VoiceFile"]];
        
        recorder =[[AVAudioRecorder alloc]initWithURL:temporaryRecFile settings:nil error:nil];
        
        [recorder setDelegate:self];
        [recorder prepareToRecord];
        [recorder record];
        [prog setHidden:NO];
    
        //Wait for 7 seconds
        [self performSelector:@selector(complete) withObject:nil afterDelay:REC_TIME];

    
}




- (void)viewDidLoad
{
    isNotRecording =YES;
    recStateLabel.text=@"Scan for Whispers";
    
    AVAudioSession *audioSession = [AVAudioSession sharedInstance];
    
    [audioSession setCategory:AVAudioSessionCategoryRecord error:nil];
    
    [audioSession setActive:YES error:nil];
    
    [prog setProgress:0.0];
    [prog setHidden:YES];
    
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)viewDidUnload{
    NSFileManager *fileHandler = [NSFileManager defaultManager];
    [fileHandler removeItemAtURL:temporaryRecFile error:nil];
    [recorder dealloc];
    recorder = nil;
    temporaryRecFile = nil;
}

- (void)dealloc {
    [recButton release];
    [recStateLabel release];
    [prog release];
    
    [super dealloc];
    
}

@end
