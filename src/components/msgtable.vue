<template>
    <div>
        <p class="demonstration" style="font-weight: bold;">Date Selector</p>
        <el-date-picker v-model="timerange" type="daterange" range-separator="To" start-placeholder="Start date"
            end-placeholder="End date" format="YYYY/MM/DD" value-format="x" @change="querymsg_time" />
    </div>

    <div>
        <p class="demonstration" style="font-weight: bold;">Keyword Selector</p>
        <el-input v-model="keywd" @input="querymsg_key" style="width:300px" />
    </div>

    <div style="margin:50px auto 0 auto">
        <el-table :data="chatData" :table-layout="tableLayout" style="width: 100%;">
            <el-table-column prop="is_send" label="Sender">
                <template #default="scope">
                    <div v-if="scope.row.is_send == '1'"><el-avatar :src="xx" /></div>
                    <div v-else><el-avatar :src="wc" /></div>
                </template>
            </el-table-column>

            <el-table-column prop="text" label="Content">
                <template #default="scope">
                    <div class="break-word">

                        <div v-if="scope.row.type == '1'">{{ scope.row.text }}</div>

                        <div v-else-if="scope.row.type == '3'">
                            <el-button v-if="scope.row.text.charAt(0) === '.'" type="primary"
                                @click="openimg(scope.row.text)" style="margin: 0 10px 0 0" round>
                                <el-icon>
                                    <Picture />
                                </el-icon>&nbsp;查看图片
                            </el-button>
                            <el-button v-else-if="scope.row.text.charAt(0) === 'h'" type="primary"
                                @click="openimg(scope.row.text)" style="margin: 0 10px 0 0" round>
                                <el-icon>
                                    <ChatLineRound />
                                </el-icon>&nbsp;查看表情包
                            </el-button>
                        </div>

                        <div v-else-if="scope.row.type == '34'">
                            <el-button type="warning" @click="open_voice(scope.row.text)" style="margin: 0 10px 0 0" round>
                                <el-icon>
                                    <Microphone />
                                </el-icon>&nbsp;播放语音
                            </el-button>
                        </div>

                        <div v-else-if="scope.row.type == '43'">
                            <el-button type="success" @click="open_video(scope.row.text)" style="margin: 0 10px 0 0" round>
                                <el-icon>
                                    <VideoPlay />
                                </el-icon>&nbsp;播放视频
                            </el-button>
                        </div>

                        <div v-else-if="scope.row.type == '49' && scope.row.subtype == '3'">
                            <el-button type="success" style="margin: 0 10px 0 0">
                                <el-link :href=scope.row.link_url style="color:white"><el-icon>
                                        <Headset />
                                    </el-icon>&nbsp;{{ scope.row.artist }}&nbsp;-&nbsp;{{ scope.row.title }}</el-link>
                            </el-button>
                            <el-tag type="info">Source: {{ scope.row.website_name }}</el-tag>
                        </div>

                        <div v-else-if="scope.row.type == '49' && scope.row.subtype == '3'">
                            <el-button type="success" style="margin: 0 10px 0 0">
                                <el-link :href=scope.row.link_url style="color:white"><el-icon>
                                        <Headset />
                                    </el-icon>&nbsp;{{ scope.row.artist }}&nbsp;-&nbsp;{{ scope.row.title }}</el-link>
                            </el-button>
                            <el-tag type="info">Source: {{ scope.row.website_name }}</el-tag>
                        </div>

                        <div v-else-if="scope.row.type == '49' && scope.row.subtype == '5'">
                            <el-card shadow="hover">
                                <el-link :href=scope.row.url>
                                    <h3>{{ scope.row.title }}</h3>
                                </el-link>
                                <p style="color:">{{ scope.row.description }}</p>
                            </el-card>
                            <el-tag type="info">Source: {{ scope.row.app_name }}</el-tag>
                        </div>

                        <div v-else-if="scope.row.type == '49' && scope.row.subtype == '57'">
                            <p>{{ scope.row.text }}</p>
                            <p v-if="scope.row.refer_text !== null"><el-tag type="info">{{ scope.row.refer_text }}</el-tag>
                            </p>
                            <p v-else><el-tag type="info">引用内容不支持显示</el-tag></p>
                        </div>

                        <div v-else-if="scope.row.type == '49' && scope.row.subtype == '6'">
                            <el-button type="primary" style="margin: 0 10px 0 0">
                                <el-link :href=download_url(scope.row.text) style="color:white"><el-icon>
                                        <Download />
                                    </el-icon>&nbsp;{{ scope.row.text.substring(7) }}</el-link>
                            </el-button>
                        </div>

                        <div v-else-if="scope.row.type == '0'">
                            <p><el-tag type="info">{{ scope.row.text }}</el-tag></p>
                        </div>

                    </div>
                </template>
            </el-table-column>

            <el-table-column prop="timestamp" label="Time">
                <template #default="scope">
                    <div>{{ parseTime(scope.row.timestamp) }}</div>
                </template>
            </el-table-column>
        </el-table>

        <div style="position: relative; margin: 30px auto; ">
            <el-pagination v-model:current-page.sync="current_page" layout="prev, pager, next" :total="1000"
                @update:current-page="querymsg_page" />
        </div>
    </div>

    <el-dialog v-model="dialogImageVisible" width="50%">
        <el-image :src="img_url" fit="contain" style="margin: 10px 0 0 0"></el-image>
    </el-dialog>

    <el-dialog v-model="dialogVoiceVisible" width="400px" top="200px">
        <audio :src="voice_url" controls autoplay></audio>
    </el-dialog>

    <el-dialog v-model="dialogVideoVisible" width="50% ">
        <video :src="video_url" id='v1' controls autoplay></video>
    </el-dialog>
</template>

<script lang="ts" setup>
import axios from 'axios'
import { Ref, ref } from 'vue'
import xx from "./assets/xx.png"
import wc from "./assets/wc.png"
import { Picture, Microphone, VideoPlay, Headset, Download, ChatLineRound } from "@element-plus/icons-vue"
import { OSS_BASE_URL, API_BASE_URL_DEV } from "../constants/strings"

const tableLayout = ref('auto')

const timerange = ref(['', ''])
const keywd = ref('')
const current_page = ref(1)

var state: "time" | "key" | "no" = "no"

var start_time: number = 0
var end_time: number = 0
var key_word: string = ''

const chatData: Ref<any[]> = ref([]);
const img_url: Ref<string> = ref('');
const voice_url: Ref<string> = ref('');
const video_url: Ref<string> = ref('');

const dialogImageVisible = ref(false);
const dialogVoiceVisible = ref(false);
const dialogVideoVisible = ref(false);

const querymsg_time = (timerange: [string, string]) => {
    state = "time";
    start_time = parseInt(timerange[0]) / 1000;
    end_time = parseInt(timerange[1]) / 1000;
    axios.get(API_BASE_URL_DEV + '/QueryByTime', {
        params: {
            token: window.localStorage.getItem('access_token'),
            start: start_time,
            end: end_time,
            page: 1,
            pagesize: 20
        }
    })
        .then(function (res) {
            chatData.value = res.data.data;
            current_page.value = 1;
            keywd.value = '';
        })
        .catch(function (err) {
            console.log(err);
        });
}

const querymsg_key = (keywd: string) => {
    state = "key";
    key_word = keywd;
    axios.get(API_BASE_URL_DEV + '/QueryByKeyword', {
        params: {
            token: window.localStorage.getItem('access_token'),
            key: key_word,
            page: 1,
            pagesize: 20
        }
    })
        .then(function (res) {
            chatData.value = res.data.data;
            current_page.value = 1;
            timerange.value = ['', ''];
        })
        .catch(function (err) {
            console.log(err);
        });
}

const querymsg_page = (current_page: number) => {
    if (start_time && end_time && state === 'time') {
        state = "time";
        axios.get(API_BASE_URL_DEV + '/QueryByTime', {
            params: {
                token: window.localStorage.getItem('access_token'),
                start: start_time,
                end: end_time,
                page: current_page,
                pagesize: 20
            }
        })
            .then(function (res) {
                chatData.value = res.data.data;
            })
            .catch(function (err) {
                console.log(err);
            });
    }
    if (key_word.length && state === 'key') {
        state = "key";
        axios.get(API_BASE_URL_DEV + '/QueryByKeyword', {
            params: {
                token: window.localStorage.getItem('access_token'),
                key: key_word,
                page: current_page,
                pagesize: 20
            }
        })
            .then(function (res) {
                chatData.value = res.data.data;
            })
            .catch(function (err) {
                console.log(err);
            });
    }
}

const parseTime = (tick: string) => {
    const tick_num = parseInt(tick) * 1000;
    const date = new Date(tick_num);
    const dateString = date.toLocaleDateString('cn', { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' });
    return dateString
}

const openimg = (url: string) => {
    if (url.charAt(0) === '.')
        img_url.value = OSS_BASE_URL + url.substring(1);
    else img_url.value = url.substring(5);
    dialogImageVisible.value = true;
}

const open_voice = (url: string) => {
    voice_url.value = OSS_BASE_URL + url.substring(1);
    dialogVoiceVisible.value = true;
}

const open_video = (url: string) => {
    video_url.value = OSS_BASE_URL + url.substring(1);
    dialogVideoVisible.value = true;
}

const download_url = (url: string) => {
    return (OSS_BASE_URL + url.substring(1));
}
</script>

<style lang="scss" scoped>
.break-word {
    word-break: break-all;
    overflow-wrap: break-word;
}
</style>