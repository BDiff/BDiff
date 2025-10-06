/*
Copyright (c) [2025] [Song Wansheng, Lu Yao]
BDiff is licensed under Mulan PubL v2.
You can use this software according to the terms and conditions of the Mulan PubL v2.
You may obtain a copy of Mulan PubL v2 at:
         http://openworks.mulanos.cn/#/licenses/MulanPubL-v2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PubL v2 for more details.
*/

import fs from "node:fs";
import path from "node:path";
import { exec } from "child_process";
import chalk from "chalk";
import qiniu from "qiniu";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const log = console.log;

const accessKey = "954-PH1tShNDppTvXjh6v-HAunL45MzZPqAWGP35";
const secretKey = "mkCGvQqyvr28XgH9RSvbMKKukmrM4z0s9VBeDUCs";
const mac = new qiniu.auth.digest.Mac(accessKey, secretKey);

const config = new qiniu.conf.Config();
config.zone = qiniu.zone.Zone_z2; // 华南

const formUploader = new qiniu.form_up.FormUploader(config);

function upload(key: string, localFile: string) {
  const options = {
    scope: "bdiff-refactoring",
  };
  const putPolicy = new qiniu.rs.PutPolicy(options);
  const uploadToken = putPolicy.uploadToken(mac);

  return formUploader.putFile(uploadToken, key, localFile, null);
}

async function walkPath(filepath: string, callback: { (filepath: string) }) {
  const stats = fs.statSync(filepath);
  if (stats.isDirectory()) {
    const filenames = fs.readdirSync(filepath);
    for (const filename of filenames) {
      await walkPath(path.join(filepath, filename), callback);
    }
  } else {
    await callback(filepath);
  }
}

async function main() {
  const startPath = path.join(__dirname, "dist");
  const filePaths = [];
  let count_done = 0;

  await walkPath(startPath, function (filepath) {
    filePaths.push(filepath);
    return Promise.resolve();
  });

  for await (const filepath of filePaths) {
    const key = path.relative(startPath, filepath).replace(/\\/g, "/");

    const { resp } = await upload(key, filepath).catch((err) => {
      log(chalk.red(`[code: ${err.statusCode}]`), key);
      throw err;
    });

    if (resp.statusCode !== 200) {
      log(chalk.yellow(`[code: ${resp.statusCode}]: ${key}`));
    }

    count_done += 1;

    process.stdout.write(`...[${count_done}/${filePaths.length}] 正在上传资源 \r`);
  }

  log(chalk.green(`[${count_done}/${filePaths.length}]`), `上传结束`, startPath);
  exec(`start "" "${startPath.replace(/ /g, " ")}"`);
}

main().finally(() => {});
