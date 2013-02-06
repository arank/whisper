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
    [prog setHidden:YES];
    [prog stopAnimating];
    recStateLabel.text=@"Sending";
    [recorder stop];
    
    
    dispatch_async( dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        
        
        
        NSString *urlString = @"http://169.254.83.201:8000/upload";/////////////////MAKE STATIC IP
        
        NSString *filename= [temporaryRecFile absoluteString];
        
        

        NSMutableURLRequest *request= [[[NSMutableURLRequest alloc] init] autorelease];
        [request setURL:[NSURL URLWithString:urlString]];
        [request setHTTPMethod:@"POST"];
        NSString *boundary = @"---------------------------14737809831466499882746641449";
        NSString *contentType = [NSString stringWithFormat:@"multipart/form-data; boundary=%@",boundary];
        [request addValue:contentType forHTTPHeaderField: @"Content-Type"];
        NSMutableData *postbody = [NSMutableData data];
        [postbody appendData:[[NSString stringWithFormat:@"\r\n--%@\r\n",boundary] dataUsingEncoding:NSUTF8StringEncoding]];
        [postbody appendData:[[NSString stringWithFormat:@"Content-Disposition: form-data; name=\"userfile\"; filename=\"%@.caf\"\r\n", filename] dataUsingEncoding:NSUTF8StringEncoding]];//potentially use .caf
        [postbody appendData:[[NSString stringWithString:@"Content-Type: application/octet-stream\r\n\r\n"] dataUsingEncoding:NSUTF8StringEncoding]];
        [postbody appendData:[NSData dataWithContentsOfURL:temporaryRecFile]];
        [postbody appendData:[[NSString stringWithFormat:@"\r\n--%@--\r\n",boundary] dataUsingEncoding:NSUTF8StringEncoding]];
        [request setHTTPBody:postbody];
        
        NSData *returnData = [NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];
        NSString *returnString = [[NSString alloc] initWithData:returnData encoding:NSUTF8StringEncoding];
        
        
        dispatch_async( dispatch_get_main_queue(), ^{

            [recButton setHidden:NO];
            
            
            NSString* foo = @"err";

            if([foo isEqualToString:returnString]){
                [recStateLabel setText:@"No Whispers Found"];
            }else{
                [recStateLabel setText:@"Scan for Whispers"];
                NSURL *url = [NSURL URLWithString:returnString];
                
                if (![[UIApplication sharedApplication] openURL:url])
                    NSLog(@"%@%@",@"Failed to open url:",[url description]);
            }
    
      
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
    [prog startAnimating];
    [self performSelector:@selector(complete) withObject:nil afterDelay:REC_TIME];

    
    
    
}




- (void)viewDidLoad
{
    isNotRecording =YES;
    recStateLabel.text=@"Scan for Whispers";
    
    AVAudioSession *audioSession = [AVAudioSession sharedInstance];
    
    [audioSession setCategory:AVAudioSessionCategoryRecord error:nil];
    
    [audioSession setActive:YES error:nil];
    
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
