Attribute VB_Name = "ModuleMain"
Option Explicit

Sub Main()
    If Not (Dir(Environ("SystemDrive") & "\Program Files\Microsoft\EdgeWebView", vbDirectory) <> "" Or _
            Dir(Environ("SystemDrive") & "\Program Files (x86)\Microsoft\EdgeWebView", vbDirectory) <> "") Then
        NotFoundError "Microsoft Edge WebView2 runtime", "EdgeWebView"
    End If

    If Not Dir(App.Path & "\smm2helper.py") <> "" Then
        NotFoundError "SMM2Helper", "smm2helper"
    End If
    
    If Dir(App.Path & "\Python", vbDirectory) <> "" Then
        If Dir(App.Path & "\Python\pythonw.exe") <> "" Then
            Shell """" & App.Path & "\Python\pythonw.exe" & """ """ & App.Path & "\smm2helper.py" & """", vbHide
        Else
            NotFoundError "Python executable", "Python\pythonw.exe"
        End If
    Else
        NotFoundError "Python", "Python"
    End If
End Sub

Sub NotFoundError(NotFoundName As String, NotFoundPath As String)
    MsgBox NotFoundName & " not found! (" & NotFoundPath & ")", vbCritical
    End
End Sub
