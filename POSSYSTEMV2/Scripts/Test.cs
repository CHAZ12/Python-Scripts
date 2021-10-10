using System;
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon.Common.Interfaces;
using UnityEngine.UIElements;

namespace VRCPOSSYSTEM
{
    public class Test : UdonSharpBehaviour
    {
        private int localPlayerID = -1;
        private VRCPlayerApi[] players = new VRCPlayerApi[81];
        public VRCPlayerApi localPlayer;
        public int networkingLocalPlayerID;
        // public TextMeshProUGUI player1ScoreText;
        // public TextMeshProUGUI player2ScoreText;

        public int[] ids = null;
        // public TextMeshProUGUI player1MenuText;
        // public TextMeshProUGUI player2MenuText;
        private float SCA = 20000.00f; // Starting customer amount
        private float SBA = 40000.00f; //Starting bar Amount

        public Text cusAccount;
        public Text barAccount;
        public Text cusName;
        public Text barName;
        private string localPlayerName;
        public Text playerDataDisplays;
        // public bool isSignedUpToPlay;
        //SYNCED VAR
        [UdonSynced] public string futureCanvasText;

        [UdonSynced] private float barAmount = 0;

        [UdonSynced] private int CusAmount;

        [UdonSynced] public float[] AmountArray;

        [UdonSynced] public string strCusName;
        [UdonSynced] public string strBarName;
        // public PosSystemV2 manager;

        public void Start()
        {
            if (Networking.LocalPlayer == null) return;
            localPlayer = Networking.LocalPlayer;
            networkingLocalPlayerID = localPlayer.playerId;
            localPlayerName = localPlayer.displayName;
            UpdateText();
        }
        private void InitializeIdsIfNull()
        {
            if (ids == null)
            {
                ids = new int[80];
                for (int i = 0; i < ids.Length; i++)
                {
                    // Assuming that the player ID does not contain -1, leave -1 blank. 
                    ids[i] = -1;
                }
            }
        }
        public override void OnPlayerJoined(VRCPlayerApi player)
        {
            Debug.LogWarning("Onjoined Fired");
            InitializeIdsIfNull();

            for (int i = 0; i < ids.Length; i++)
            {
                if (ids[i] == -1)
                {
                    ids[i] = player.playerId;
                    Debug.LogWarning("Player ID NUMBER" + ids[i]);
                    break;
                }
            }
            Start();
            UpdateArray();
        }
        public override void OnPlayerLeft(VRCPlayerApi player)
        {
            Debug.LogWarning("OnLeft Fired");
            InitializeIdsIfNull();

            for (int i = 0; i < ids.Length; i++)
            {
                if (ids[i] == player.playerId)
                {
                    ids[i] = -1;
                    break;
                }
            }
            UpdateArray();

        }
        // Create a new length of an array becuae lists is not supported yet ;( (Note I need 2 arrays inorder to get values from player joining or leaving)
        public void UpdateArray()
        {
            Debug.LogWarning("updateArray fired");
            for (int i = 0; i < ids.Length; i++)
            {
                if (ids[i] != -1)
                {
                    AmountArray = new float[i + 1];
                }
            }
        }
        public void JoinGame()
        {
            /* Networking.SetOwner(localPlayer, gameObject);
             /localPlayerID = playerNumber;

               switch (playerNumber)
               {
                   case 0:
                       player1ID = networkingLocalPlayerID;
                       Debug.Log(player1ID);
                       break;
                   case 1:
                       player2ID = networkingLocalPlayerID;
                       Debug.Log(player2ID);
                       break;
                   default:
                       return;
             */
            DoStuff();
        }
        public void UpdateText()
        {
            float Array = 0;
            futureCanvasText = ""; // Set to true to see all logs
            futureCanvasText = "---Player Lsit---\r\n";
            VRCPlayerApi.GetPlayers(players);
            //foreach (VRCPlayerApi player in players)
            // {
            for (int i = 0; i < ids.Length; i++)
            {
                if (ids[i] != -1)
                {
                    // if (player == null) continue;
                    var player = VRCPlayerApi.GetPlayerById(ids[i]);
                    int localPlyrId = Int32.Parse(player.GetPlayerTag("PID"));
                    if (AmountArray.Length == 0)
                    {
                        Debug.LogWarning("Their is no elments in array");
                    }
                    else
                    {
                        Array = AmountArray[localPlyrId] - 1;
                        Debug.LogWarning("their is an elemnt in the array");
                    }
                    futureCanvasText += string.Format("Name:{0},PID:${1}, CusAmount:{2}, BarAmount:{3}, ID#:{4}\r\n", player.displayName, player.GetPlayerTag("PID"), CusAmount, barAmount, player.playerId, Array);
                    playerDataDisplays.text = futureCanvasText.ToString();
                    Debug.Log(player.displayName);
                }
                //RequestSerialization();
            }
        }
        // Update displays for users
        public void UpdateMainMenu(int player1ID, int player2ID)
        {
            bool found = false;
            if (player1ID > 0)
            {
                int PID = 0;
                // found = HandlePlayerState(player1MenuText, player1ScoreText, VRCPlayerApi.GetPlayerById(player1ID));
            }
            else
            if (player2ID > 0)
            {
                int PID = 1;
                //   found = HandlePlayerState(player2MenuText, player2ScoreText, VRCPlayerApi.GetPlayerById(player2ID), PID);

            }
            else
            if (!found) Debug.LogWarning("NO PLAYERS");
        }
        //  public bool HandlePlayerState(TextMeshProUGUI menuText, TextMeshProUGUI scoreText, VRCPlayerApi player)
        // {
        // if (PID == 1) player.SetPlayerTag("bob", 1.ToString());
        // else player.SetPlayerTag("bob", 2.ToString());
        // menuText.text = player.displayName;
        // scoreText.text = player.displayName + "p1: " + player1ID + ", p2: " + player2ID + ", BOB:" + AmountArray[PID];
        //  menuText.text = "";
        //  for (int i = 0; i < AmountArray.Length; i++) menuText.text += "PlayerID: " + i + " " + player.displayName + ", " + AmountArray[i].ToString() + localPlayer.playerId + ",\n ";

        // if (player.playerId == Networking.LocalPlayer.playerId) return true;
        //  return false;
        //  }
        public void PlusBar()// Start settings values for Bar
        {
            Debug.LogWarning("BAR");
            if (localPlayer == null) return;
            if (!Networking.IsOwner(gameObject)) Networking.SetOwner(localPlayer, gameObject);
            localPlayer.SetPlayerTag("PID", 2.ToString());

            if (localPlayer.GetPlayerTag("PID") == 2.ToString())
            {
                barAccount.text = "Acct:$" + barAmount.ToString();
                Debug.LogWarning("PlusBar Fired");
                strBarName = localPlayerName;
                barName.text = strBarName;
                RequestSerialization();
                DoStuff();
            }
        }
        public void PlusCus()
        {
            Debug.LogWarning("CUS");
            if (localPlayer == null) return;
            if (!Networking.IsOwner(gameObject)) Networking.SetOwner(localPlayer, gameObject);

            localPlayer.SetPlayerTag("PID", 1.ToString());
            SCA = 20000.00f;
            if (localPlayer.GetPlayerTag("NewCus") == 1.ToString())
            {
                SCA = float.Parse(localPlayer.GetPlayerTag("CusAmount"));
            }
            if (localPlayer.GetPlayerTag("PID") == 1.ToString())
            {
                // Start setting values for Customer
                localPlayer.SetPlayerTag("CusAmount", SCA.ToString());
                CusAmount = Int32.Parse(localPlayer.GetPlayerTag("CusAmount"));
                localPlayer.SetPlayerTag("NewCus", 1.ToString());
                cusAccount.text = "Acct:$" + SCA.ToString();
                Debug.LogWarning("PlusCus Fired");
                strCusName = localPlayerName;
                cusName.text = strCusName;
                RequestSerialization();
                DoStuff();
            }
        }
        public override void OnDeserialization()
        {
            Debug.LogWarning("Deserialization fired successully");
        }
        public void NetworkEventStuff()
        {
            Debug.LogWarning("Networked");
            // UpdateMainMenu(player1ID, player2ID);
            UpdateText();
        }

        public void DoStuff()
        {
            // This will be sent to all clients and run locally on each one (including the one sending
            SendCustomNetworkEvent(NetworkEventTarget.All, "NetworkEventStuff");
        }
    }
}