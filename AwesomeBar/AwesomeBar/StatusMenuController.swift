//
//  StatusMenuController.swift
//  AwesomeBar
//
//  Created by Steven Stockhamer on 4/29/18.
//  Copyright © 2018 Steven Stockhamer. All rights reserved.
//

import Cocoa

class StatusMenuController: NSObject {

    @IBOutlet weak var statusMenu: NSMenu!
    let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
    
    @IBAction func quitClicked(_ sender: NSMenuItem) {
        NSApplication.shared.terminate(self)
    }
    
    override func awakeFromNib() {
        statusItem.menu = statusMenu
        
        let icon = NSImage(named: NSImage.Name("statusIcon"))
        statusItem.image = icon
    }
}
