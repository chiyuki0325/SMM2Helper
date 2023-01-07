VERSION 5.00
Begin VB.Form FormMain 
   BackColor       =   &H80000005&
   BorderStyle     =   1  'Fixed Single
   Caption         =   "SMM2Helper"
   ClientHeight    =   1620
   ClientLeft      =   45
   ClientTop       =   390
   ClientWidth     =   4950
   BeginProperty Font 
      Name            =   "Segoe UI"
      Size            =   12
      Charset         =   0
      Weight          =   400
      Underline       =   0   'False
      Italic          =   0   'False
      Strikethrough   =   0   'False
   EndProperty
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   1620
   ScaleWidth      =   4950
   StartUpPosition =   3  '´°¿ÚÈ±Ê¡
   Visible         =   0   'False
   Begin VB.Label Label1 
      BackStyle       =   0  'Transparent
      Caption         =   "Installing Python packages, please wait..."
      Height          =   645
      Left            =   180
      TabIndex        =   0
      Top             =   210
      Width           =   4305
   End
End
Attribute VB_Name = "FormMain"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub Form_Load()
    Dim FSO As New FileSystemObject
    
    If Not (FSO.FolderExists(Environ("SystemDrive") & "\Program Files\Microsoft\EdgeWebView") Or _
            FSO.FolderExists(Environ("SystemDrive") & "\Program Files (x86)\Microsoft\EdgeWebView")) Then
        NotFoundError "Microsoft Edge WebView2 runtime", "EdgeWebView"
    End If

    If Not FSO.FileExists(Environ("SystemRoot") & "\pyw.exe") Then
        MsgBox "Python not found!" & vbCrLf & "Pleases install Python 3.10+ first.", vbCritical
        End
    End If
    
    Dim IsNintendoClientsAvaliable As Boolean
    Dim IsPythonAvaliable As Boolean
    Dim PythonVersionString As String, PythonMajorVersion As Integer, PythonMinorVersion As Integer
    Dim SubFolder As Variant
    For Each SubFolder In FSO.GetFolder(Environ("LocalAppData") & "\Programs\Python").SubFolders
        PythonVersionString = Replace(SubFolder.Name, "Python", "")
        PythonMajorVersion = Int(Left(PythonVersionString, 1))
        PythonMinorVersion = Int(Right(PythonVersionString, Len(PythonVersionString) - 1))
        If PythonMajorVersion > 3 Or (PythonMajorVersion = 3 And PythonMinorVersion >= 10) Then
            IsPythonAvaliable = True
            If FSO.FolderExists(Environ("LocalAppData") & "\Programs\Python\Python" & PythonVersionString & "\Lib\site-packages\nintendo") Then
                IsNintendoClientsAvaliable = True
            End If
        End If
    Next
    
    If Not IsPythonAvaliable Then
        MsgBox "Python 3.10+ not found!" & vbCrLf & "Pleases update your Python first.", vbCritical
        End
    End If
    
    If Not IsNintendoClientsAvaliable Then
        Me.Show
        ShellAndWait "py.exe -m pip install -r """ & App.Path & "\requirements.txt""", 1
        Me.Hide
        End
    End If
    
    If Not FSO.FileExists(App.Path & "\smm2helper.py") Then
        NotFoundError "SMM2Helper", "smm2helper"
    End If
    
    Shell "pyw.exe -X utf8 """ & App.Path & "\smm2helper.py""", vbNormalFocus
    
    End
End Sub

Sub NotFoundError(NotFoundName As String, NotFoundPath As String)
    MsgBox NotFoundName & " not found! (" & NotFoundPath & ")", vbCritical
    End
End Sub

Sub ShellAndWait(PathFile As String, DisplayMode As Integer)
    With New WshShell
        .Run PathFile, DisplayMode, True
    End With
End Sub
